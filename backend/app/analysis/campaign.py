"""Explainable Campaign Link. Weights are HEURISTICS, not fitted. Validate with scripts/evaluate_links.py on labelled pairs."""
import hashlib, hmac, re
from .. import config
from .urls import SHORTENERS

VPA_RE = re.compile(r"\b[\w.\-]{2,}@[a-z]{2,}\b", re.I)
COMMON_AFTER = 3  # indicator in >3 reports is treated as common
WEIGHTS = {"shared_vpa": 0.5, "shared_domain": 0.5, "text_similarity": 0.3, "shared_category": 0.1, "time_proximity": 0.1}

def fp(value: str) -> str:
    return hmac.new(config.hmac_key(), value.lower().encode(), hashlib.sha256).hexdigest()[:16]

def redact(norm: str) -> str:
    t = re.sub(r"(?:https?://|www\.)\S+", "[URL]", norm)
    t = VPA_RE.sub("[VPA]", t)
    t = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[EMAIL]", t)
    t = re.sub(r"(?:\+91[\s-]?)?\d{10}\b", "[PHONE]", t)
    return re.sub(r"\b\d{6,}\b", "[NUM]", t)

def indicators(norm: str, urls: list, show: bool) -> dict:
    """fingerprint -> display label. Real values only shown in live mode; stored mode shows fp prefix."""
    out = {}
    for m in VPA_RE.finditer(norm):
        v = m.group(0).lower()
        if "." not in v.split("@")[1]:
            out[("vpa", fp(v))] = v if show else "VPA#" + fp(v)[:6]
    for u in urls:
        if u["domain"] in SHORTENERS or u["trusted"]:
            continue  # shared shorteners / official sites prove nothing
        out[("domain", fp(u["domain"]))] = u["domain"] if show else "domain#" + fp(u["domain"])[:6]
    return out

def cosine(a: str, b: str) -> float:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    try:
        X = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5)).fit_transform([a, b])
        return float(cosine_similarity(X[0], X[1])[0][0])
    except ValueError:
        return 0.0

def link(a: dict, b: dict, freq: dict | None = None) -> dict:
    """a/b: {text(redacted or norm), ind:{(type,fp):label}, cats:set, ts:float|None}"""
    ev, score, hard = [], 0.0, False
    for kind, key in (("vpa", "shared_vpa"), ("domain", "shared_domain")):
        for (k, f), label in a["ind"].items():
            if k == kind and (k, f) in b["ind"]:
                n = (freq or {}).get((k, f), 0)
                if n > COMMON_AFTER:  # indicator seen in many reports: weak, could be shared infrastructure
                    ev.append({"signal": key, "points": WEIGHTS[key] / 2, "detail": f"Both contain {label}, but it appears in {n} reports (common indicator, downweighted, not a hard link)", "strength": "weak"})
                    score += WEIGHTS[key] / 2
                else:
                    ev.append({"signal": key, "points": WEIGHTS[key], "detail": f"Both messages contain {label}", "strength": "strong"})
                    score += WEIGHTS[key]; hard = True
    c = cosine(a["text"], b["text"])
    if c >= 0.5:
        pts = round(WEIGHTS["text_similarity"] * c, 3)
        ev.append({"signal": "text_similarity", "points": pts, "detail": f"Template similarity {c:.2f} (character n-gram cosine)", "strength": "weak"})
        score += pts
    shared = a["cats"] & b["cats"]
    if shared:
        ev.append({"signal": "shared_category", "points": WEIGHTS["shared_category"], "detail": "Same scam category: " + ", ".join(sorted(shared)), "strength": "weak"})
        score += WEIGHTS["shared_category"]
    if a.get("ts") and b.get("ts") and abs(a["ts"] - b["ts"]) <= 86400:
        ev.append({"signal": "time_proximity", "points": WEIGHTS["time_proximity"], "detail": "Reported within 24 hours", "strength": "weak"})
        score += WEIGHTS["time_proximity"]
    raw = round(score, 3)
    score = round(min(score, 1.0), 3)
    level = "strong" if score >= 0.6 and hard else "possible" if score >= 0.3 else "insufficient_evidence"
    note = {"strong": "Linked by a shared hard indicator plus supporting evidence.",
            "possible": "Similar, but no shared hard indicator: could be a copied template by unrelated scammers.",
            "insufficient_evidence": "Not enough evidence to link these messages."}[level]
    return {"level": level, "score": score, "raw_total": raw, "score_label": "evidence score (capped at 1.0), NOT a probability of common ownership", "evidence": ev, "explanation": note,
            "ignored_signals": "Shared URL shorteners and official domains are ignored (they link unrelated messages).",
            "weights_validated": False}
