"""Grouped cross-validation of the FULL pipeline. Writes app/data/metrics.json. Numbers come only from running this."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sklearn.model_selection import StratifiedGroupKFold
from app.analysis.classifier import load_rows, make_model
from app.analysis.normalizer import normalize
from app.analysis.pipeline import analyze
from app import config

def metrics(rows, preds):
    tp = sum(1 for r, p in zip(rows, preds) if r["label"] == "1" and p == "suspicious")
    fp = sum(1 for r, p in zip(rows, preds) if r["label"] == "0" and p == "suspicious")
    pos = sum(1 for r in rows if r["label"] == "1"); neg = len(rows) - pos
    ab = sum(1 for p in preds if p == "unable_to_verify")
    fn = pos - tp
    prec = tp / (tp + fp) if tp + fp else None
    rec = tp / pos if pos else None
    f1 = 2 * prec * rec / (prec + rec) if prec and rec else None
    cm = {}
    for r, p in zip(rows, preds):
        cm.setdefault("scam" if r["label"] == "1" else "legit", {}).setdefault(p, 0); cm["scam" if r["label"] == "1" else "legit"][p] += 1
    rd = lambda x: None if x is None else round(x, 3)
    return {"precision": rd(prec), "recall": rd(rec), "f1": rd(f1), "false_positive_rate": rd(fp / neg if neg else None),
            "abstention_rate": rd(ab / len(rows)), "tp": tp, "fp": fp, "fn": fn, "confusion": cm}

def main():
    rows = load_rows()
    # Legitimate messages have no campaign: give them small synthetic groups (chunks of 4 rows) so every fold has both classes.
    n = 0
    for r in rows:
        if r["label"] == "0":
            r["group"] = f"legit{n // 4}"; n += 1
    groups = [r["group"] for r in rows]; labels = [int(r["label"]) for r in rows]
    k = 5
    full, rules_only, ml_only = [None] * len(rows), [None] * len(rows), [None] * len(rows)
    for tr, te in StratifiedGroupKFold(n_splits=k, shuffle=True, random_state=42).split(rows, labels, groups):
        ytr = [labels[i] for i in tr]
        m = make_model().fit([normalize(rows[i]["text"]) for i in tr], ytr) if len(set(ytr)) == 2 else None
        for i in te:
            full[i] = analyze(rows[i]["text"], model=m, use_model=m is not None)["outcome"]
            rules_only[i] = analyze(rows[i]["text"], use_model=False)["outcome"]
            ml_only[i] = ("suspicious" if m is not None and m.predict_proba([normalize(rows[i]["text"])])[0][1] >= 0.5 else "low_apparent_risk")
            if rows[i]["label"] == "1" and rules_only[i] != "suspicious": print("MISSED:", rows[i]["text"][:120])
            if rows[i]["label"] == "0" and rules_only[i] == "suspicious": print("FALSE ALARM:", rows[i]["text"][:120])
    out = {"n": len(rows), "scam": sum(r["label"] == "1" for r in rows), "legit": sum(r["label"] == "0" for r in rows),
           "split": f"StratifiedGroupKFold k={k}; scam rows grouped by campaign family, legit rows in chunks of 4",
           "full_pipeline": metrics(rows, full), "rules_only": metrics(rows, rules_only), "ml_only": metrics(rows, ml_only),
           "caveat": "Dataset is a SMALL, hand-written SEED set; rules were written by the same author, so rules_only is optimistic. Replace with real, independently labelled data before trusting these numbers."}
    json.dump(out, open(config.DATA / "metrics.json", "w"), indent=2)
    print(json.dumps(out, indent=2))
def challenge(path):
    import csv
    dev = load_rows(); m = make_model().fit([normalize(r["text"]) for r in dev], [int(r["label"]) for r in dev])
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8-sig", newline="")) if r.get("text") and r.get("label") in ("0", "1")]
    full = [analyze(r["text"], model=m)["outcome"] for r in rows]; ro = [analyze(r["text"], use_model=False)["outcome"] for r in rows]
    by = {}
    for r, p in zip(rows, full): by.setdefault(r.get("kind", "?"), []).append((r, p))
    out = {"n": len(rows), "source_file": path, "rules_frozen_note": "Run ONLY after freezing rules. Do not tune on this file and still call it independent.",
           "full_pipeline": metrics(rows, full), "rules_only": metrics(rows, ro),
           "by_kind": {k: metrics([x[0] for x in v], [x[1] for x in v]) for k, v in by.items()}}
    json.dump(out, open(config.DATA / "metrics_challenge.json", "w"), indent=2); print(json.dumps(out, indent=2))

if len(sys.argv) > 2 and sys.argv[1] == "--challenge": challenge(sys.argv[2])
else: main()
