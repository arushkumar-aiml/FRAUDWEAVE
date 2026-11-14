from .analysis.pipeline import analyze
from .analysis.campaign import redact, indicators, fp, link
from . import db

def store_report(text: str, ts=None) -> dict:
    res = analyze(text); norm = res["_norm"]
    red = redact(norm)
    if res["outcome"] != "suspicious":
        return {"stored": False, "reason": "Only messages assessed as suspicious are stored."}
    ok = db.add_report(res, red, indicators(norm, _with_trust(res), False), fp(red), ts)
    return {"stored": ok, "duplicate": not ok}

def _with_trust(res):
    from .analysis.urls import _is_official
    return [dict(u, trusted=_is_official(u["domain"])) for u in res["urls"]]

def side(text: str, show=True) -> dict:
    res = analyze(text); n = res["_norm"]
    return {"text": redact(n), "ind": indicators(n, _with_trust(res), show),
            "cats": set(res["categories"]), "ts": None}

def _brief(g, links):
    counts = {}
    for r in g:
        for lbl in r["ind"].values(): counts[lbl] = counts.get(lbl, 0) + 1
    shared = sorted(l for l, n in counts.items() if n >= 2)
    cats = ", ".join(sorted(set().union(*[r["cats"] for r in g]))) or "uncategorised"
    return {"title": f"Suspected scam campaign: {cats}", "report_count": len(g), "shared_indicators": shared,
            "template_sample": g[0]["text"][:200],
            "victim_advice": ["Do not click links, share OTP/PIN, or pay.", "Verify via the official app or the number on your card.",
                              "If money was lost, call 1930 immediately.", "Report at https://cybercrime.gov.in"],
            "report_text": f"{len(g)} similar scam messages (category: {cats}) were reported. Shared indicators (fingerprints only, raw values withheld): {', '.join(shared) or 'none'}. Example template: {g[0]['text'][:160]}",
            "disclaimer": "Linked by an evidence score, not proof of a single offender."}

def clusters():
    reps = db.all_reports(); rv = db.reviews(); parent = list(range(len(reps)))
    freq = {}
    for r in reps:
        for k in r["ind"]: freq[k] = freq.get(k, 0) + 1
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    links = []
    for i in range(len(reps)):
        for j in range(i + 1, len(reps)):
            key = tuple(sorted((reps[i]["id"], reps[j]["id"]))); d = rv.get(key)
            if d == "reject": continue  # human reviewer rejected this link
            r = link(reps[i], reps[j], freq)
            if d == "accept": r["level"] = "strong"; r["explanation"] = "Accepted by a human reviewer."
            if r["level"] != "insufficient_evidence":
                links.append({"a": reps[i]["id"], "b": reps[j]["id"], "review": d, **r})
            if r["level"] == "strong": parent[find(i)] = find(j)  # only STRONG links merge clusters
    groups = {}
    for i, r in enumerate(reps): groups.setdefault(find(i), []).append(r)
    out = []
    for g in groups.values():
        if len(g) < 2: continue
        ids = {r["id"] for r in g}; cl = [l for l in links if l["a"] in ids and l["b"] in ids]
        out.append({"size": len(g), "report_ids": sorted(ids), "categories": sorted(set().union(*[r["cats"] for r in g])),
                    "sample": g[0]["text"][:160], "links": cl, "brief": _brief(g, cl)})
    possible = [l for l in links if l["level"] == "possible"]
    return {"clusters": sorted(out, key=lambda c: -c["size"]), "possible_links": possible[:20], "report_count": len(reps)}
