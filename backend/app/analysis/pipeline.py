from .normalizer import normalize
from .rules import run_rules
from .urls import analyze_urls
from .decision import decide, ACTIONS
from .classifier import scam_probability

def analyze(text: str, model=None, use_model=True) -> dict:
    norm = normalize(text)
    hits, urls = run_rules(norm), analyze_urls(norm)
    p = scam_probability(norm, model) if use_model else None
    outcome, score = decide(norm, hits, urls, p)
    cats = sorted({h["category"] for h in hits if h["category"] != "general"})
    return {"outcome": outcome, "risk_score": score,
            "model_confidence": None if p is None else round(max(p, 1 - p), 3),
            "model_scam_probability": None if p is None else round(p, 3),
            "categories": cats,
            "evidence": [{k: v for k, v in h.items() if k != "strong"} for h in hits],
            "urls": [{k: v for k, v in u.items() if k != "trusted"} for u in urls],
            "recommended_actions": ACTIONS if outcome != "low_apparent_risk" else ["No red flags found by our rules, but this is not a guarantee. Stay careful."],
            "disclaimer": "Risk score is not a calibrated probability. model_confidence is uncalibrated.",
            "_norm": norm}
