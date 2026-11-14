"""TF-IDF + Logistic Regression. Trained locally from data/dataset.csv. Probabilities are NOT calibrated."""
import csv
from ..config import DATA
from .normalizer import normalize

def make_model():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    return make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), lowercase=True, sublinear_tf=True),
                         LogisticRegression(max_iter=1000, class_weight="balanced"))

def load_rows():
    with open(DATA / "dataset.csv", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    good = [r for r in rows if r.get("text") and r.get("label") in ("0", "1") and r.get("group")]
    if len(good) != len(rows):
        print(f"WARNING: skipped {len(rows) - len(good)} malformed row(s)")
    return good

_MODEL = None
def get_model():
    global _MODEL
    if _MODEL is None:
        rows = load_rows()
        _MODEL = make_model().fit([normalize(r["text"]) for r in rows], [int(r["label"]) for r in rows])
    return _MODEL

def scam_probability(norm: str, model=None):
    try:
        m = model or get_model()
        return float(m.predict_proba([norm])[0][1])
    except Exception:
        return None
