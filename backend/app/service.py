import json
from .analysis.pipeline import analyze
from .analysis.campaign import redact, indicators, fp, link
from . import db

def store_report(text: str, ts=None) -> dict:
    res = analyze(text); norm = res["_norm"]
    red = redact(norm)
    if res["outcome"] != "suspicious":
        return {"stored": False, "reason": "Only messages assessed as suspicious are stored."}
    rid = db.add_report(res, red, indicators(norm, _with_trust(res), False), fp(red), ts)
    return {"stored": rid is not None, "duplicate": rid is None, "report_id": rid}

def _with_trust(res):
    from .analysis.urls import _is_official
    return [dict(u, trusted=_is_official(u["domain"])) for u in res["urls"]]

def side(text: str, show=True) -> dict:
    res = analyze(text); n = res["_norm"]
    return {"text": redact(n), "ind": indicators(n, _with_trust(res), show),
            "cats": set(res["categories"]), "ts": None}

import datetime
DECISIONS = {"accept": "accepted", "reject": "rejected", "insufficient_evidence": "insufficient_evidence"}

def _iso(ts): return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def review(a: int, b: int, decision: str, note: str = ""):
    if a == b: raise ValueError("A report cannot be linked to itself.")
    if decision not in DECISIONS: raise ValueError("decision must be accept, reject or insufficient_evidence.")
    if len(note) > 500: raise ValueError("Note is too long (max 500 characters).")
    for i in (a, b):
        if not db.report_exists(i): raise LookupError(f"Report {i} not found.")
    return db.add_review(a, b, decision, note.strip())

def _blocked(p):
    return p["status"] in ("rejected", "insufficient_evidence") or (p["level"] == "insufficient_evidence" and p["status"] != "accepted")

def _brief(cid, g, rels):
    counts = {}
    for r in g:
        for lbl in r["ind"].values(): counts[lbl] = counts.get(lbl, 0) + 1
    shared = sorted(l for l, n in counts.items() if n >= 2)
    cats = ", ".join(sorted(set().union(*[r["cats"] for r in g]))) or "uncategorised"
    top = max(rels, key=lambda x: x["score"]) if rels else None
    status = {}
    for x in rels: status[x["status"]] = status.get(x["status"], 0) + 1
    ts = [r["ts"] for r in g]
    return {"campaign_id": cid, "title": f"Suspected scam campaign: {cats}", "report_count": len(g), "report_ids": sorted(r["id"] for r in g),
            "categories": sorted(set().union(*[r["cats"] for r in g])), "observed_from": _iso(min(ts)), "observed_to": _iso(max(ts)),
            "shared_indicators": shared, "templates": [r["text"][:220] for r in sorted(g, key=lambda r: r["id"])[:3]],
            "evidence_score": top["score"] if top else None, "evidence_breakdown": top["evidence"] if top else [],
            "explanation": top["explanation"] if top else "No qualifying relationship recorded.",
            "review_status": status or {"pending": 0},
            "victim_advice": ["Do not click links, share OTP/PIN, or pay.", "Verify via the official app or the number on your card.",
                              "If money was lost, call 1930 immediately.", "Report at https://cybercrime.gov.in"],
            "report_text": f"{len(g)} similar scam messages (category: {cats}) were reported between {_iso(min(ts))} and {_iso(max(ts))}. Shared indicators (fingerprints only, raw values withheld): {', '.join(shared) or 'none'}. Example template: {g[0]['text'][:160]}",
            "links": {"cybercrime_portal": "https://cybercrime.gov.in/", "helpline": "1930"},
            "disclaimer": "Linked by an evidence score, not proof of a single offender. Never submitted automatically."}

def clusters():
    reps = sorted(db.all_reports(), key=lambda r: r["id"]); rv = db.latest_reviews()
    freq = {}
    for r in reps:
        for k in r["ind"]: freq[k] = freq.get(k, 0) + 1
    pairs = {}
    for i in range(len(reps)):
        for j in range(i + 1, len(reps)):
            a, b = reps[i]["id"], reps[j]["id"]; p = link(reps[i], reps[j], freq); rev = rv.get((a, b))
            p.update({"a": a, "b": b, "status": DECISIONS.get(rev["decision"], "pending") if rev else "pending",
                      "note": rev["note"] if rev else "", "reviewed_at": _iso(rev["ts"]) if rev else None})
            p["effective"] = "strong" if p["status"] == "accepted" else p["level"]
            if p["status"] in ("rejected", "insufficient_evidence"): p["effective"] = p["status"]
            pairs[(a, b)] = p
    groups = {r["id"]: frozenset([r["id"]]) for r in reps}
    cands = sorted([k for k, p in pairs.items() if p["effective"] == "strong"], key=lambda k: (-pairs[k]["score"], k))
    for a, b in cands:  # complete-link: merge only if NO cross pair is rejected/insufficient/unsupported
        ga, gb = groups[a], groups[b]
        if ga == gb: continue
        if any(_blocked(pairs[tuple(sorted((x, y)))]) for x in ga for y in gb): continue
        new = ga | gb
        for m in new: groups[m] = new
    byid = {r["id"]: r for r in reps}; out = []
    for g in sorted({g for g in groups.values() if len(g) > 1}, key=min):
        members = [byid[i] for i in sorted(g)]; rels = [p for k, p in pairs.items() if k[0] in g and k[1] in g and p["level"] != "insufficient_evidence"]
        out.append({"campaign_id": "C-%04d" % min(g), "size": len(g), "report_ids": sorted(g), "categories": sorted(set().union(*[m["cats"] for m in members])),
                    "brief": _brief("C-%04d" % min(g), members, rels)})
    rel = [p for p in pairs.values() if p["level"] != "insufficient_evidence" or p["status"] != "pending"]
    rel = [{k: v for k, v in p.items() if k != "effective"} for p in sorted(rel, key=lambda p: (-p["score"], p["a"], p["b"]))]
    return {"clusters": out, "relationships": rel, "report_count": len(reps)}

def stats():
    from . import config
    c = db.conn(); rows = c.execute("SELECT id,created,categories,outcome,risk FROM reports ORDER BY id DESC").fetchall(); c.close()
    cats = {}
    for r in rows:
        for k in json.loads(r["categories"]): cats[k] = cats.get(k, 0) + 1
    shown = {k: v for k, v in cats.items() if v >= config.MIN_CATEGORY_COUNT}
    d = clusters(); st = {"pending": 0, "accepted": 0, "rejected": 0, "insufficient_evidence": 0}
    for p in d["relationships"]: st[p["status"]] += 1
    return {"total_reports": len(rows), "suspicious_reports": sum(1 for r in rows if r["outcome"] == "suspicious"), "campaigns": len(d["clusters"]),
            "relationships": st, "categories": shown, "categories_hidden_below_threshold": len(cats) - len(shown), "threshold": config.MIN_CATEGORY_COUNT,
            "recent": [{"id": r["id"], "time": _iso(r["created"]), "categories": json.loads(r["categories"]), "outcome": r["outcome"], "risk": r["risk"]} for r in rows[:8]]}
