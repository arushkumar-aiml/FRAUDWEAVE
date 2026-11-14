import json
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from . import config, service, db
from .schemas import AnalyzeRequest, ReportRequest, LinkRequest, ReviewRequest
from .analysis.pipeline import analyze
from .analysis.campaign import link

app = FastAPI(title="FraudWeave", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=config.ALLOWED_ORIGINS, allow_methods=["GET", "POST"], allow_headers=["*"])

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/api/v1/analyze")
def analyze_ep(req: AnalyzeRequest):
    if not req.text.strip(): raise HTTPException(422, "text must not be blank")
    r = analyze(req.text); r.pop("_norm"); return r

_HITS: dict = {}
def _rate_limit(ip: str, limit=20, window=3600):
    now = time.time(); hits = [t for t in _HITS.get(ip, []) if now - t < window]
    if len(hits) >= limit: raise HTTPException(429, "Too many reports from this address. Try later.")
    hits.append(now); _HITS[ip] = hits

@app.post("/api/v1/reports")
def report(req: ReportRequest, request: Request):
    _rate_limit(request.client.host if request.client else "unknown")
    if not req.consent: raise HTTPException(400, "Consent is required to store a report.")
    return service.store_report(req.text)

@app.post("/api/v1/campaigns/link")
def link_ep(req: LinkRequest):
    return link(service.side(req.a), service.side(req.b))

@app.get("/api/v1/campaigns")
def campaigns():
    d = service.clusters()
    c = db.conn(); rows = c.execute("SELECT categories FROM reports").fetchall(); c.close()
    counts = {}
    for r in rows:
        for k in json.loads(r["categories"]): counts[k] = counts.get(k, 0) + 1
    d["trends"] = {k: v for k, v in counts.items() if v >= config.MIN_CATEGORY_COUNT}
    d["trend_min_reports"] = config.MIN_CATEGORY_COUNT
    return d

@app.get("/api/v1/metrics")
def metrics():
    f = config.DATA / "metrics.json"
    return json.load(open(f)) if f.exists() else {"available": False, "hint": "Run: python scripts/evaluate.py"}

@app.post("/api/v1/campaigns/review")
def review(req: ReviewRequest):
    db.set_review(req.a, req.b, req.decision); return {"saved": True}
