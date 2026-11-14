import json, re
from ..config import DATA
_NEG = re.compile(r"(do not|don't|dont|never|mat|na|nahi|kabhi nahi)\s*$", re.I)

def _load():
    rules = json.load(open(DATA / "rules.json", encoding="utf-8"))
    for r in rules:
        r["_re"] = [re.compile(p, re.I) for p in r["patterns"]]
    return rules
RULES = _load()

def run_rules(norm: str) -> list[dict]:
    """Return one evidence item per rule (first non-negated match), with exact span in `norm`."""
    out = []
    for r in RULES:
        for rx in r["_re"]:
            hit = None
            for m in rx.finditer(norm):
                before = norm[max(0, m.start() - 20):m.start()]
                if r["strong"] and _NEG.search(before):
                    continue  # "do not share OTP" is a warning, not a request
                hit = m
                break
            if hit:
                out.append({"rule_id": r["id"], "category": r["category"], "matched_text": hit.group(0),
                            "start": hit.start(), "end": hit.end(), "reason": r["reason"],
                            "weight": r["weight"], "strong": r["strong"]})
                break
    return out
