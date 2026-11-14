from .normalizer import supported_script_ratio
from .urls import POINTS

ACTIONS = ["Do not click links, share OTP/PIN, or pay anything because of this message.",
           "Verify independently using the official app or the number printed on your card.",
           "If money was lost, call 1930 immediately.",
           "Report at https://cybercrime.gov.in"]

def decide(norm, hits, urls, model_prob=None):
    score = sum(h["weight"] for h in hits)
    for u in urls:
        score += sum(POINTS[f] for f in u["flags"])
    score = min(100, score)
    strong = any(h["strong"] for h in hits) or any("known_bad" in u["flags"] for u in urls)
    untrusted_url = any(not u["trusted"] for u in urls)
    risky_link = any(u["flags"] for u in urls) and any(h["weight"] >= 25 for h in hits)
    if risky_link: score = max(score, 60)  # scam signal + risky link
    if score >= 60 or strong:
        return "suspicious", max(score, 60 if strong else score)
    if len(norm) < 20 or supported_script_ratio(norm) < 0.5:
        return "unable_to_verify", score
    if score < 25 and not untrusted_url:
        if model_prob is not None and model_prob >= 0.7:
            return "unable_to_verify", score  # rules and model disagree -> abstain
        return "low_apparent_risk", score
    return "unable_to_verify", score
