import json
import time
from fastapi import FastAPI, HTTPException, Request, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import config, service, db, auth
from .schemas import AnalyzeRequest, ReportRequest, LinkRequest, ReviewRequest
from .analysis.pipeline import analyze
from .analysis.campaign import link

app = FastAPI(title="FraudWeave", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=config.ALLOWED_ORIGINS, allow_methods=["GET", "POST", "DELETE"], allow_headers=["*"])

@app.on_event("startup")
def _startup():
    import os
    if os.environ.get("FRAUDWEAVE_SEED_DEMO") == "1":
        from .demo_data import seed; seed()

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/api/v1/analyze")
def analyze_ep(req: AnalyzeRequest):
    if not req.text.strip(): raise HTTPException(422, "text must not be blank")
    r = analyze(req.text); r.pop("_norm"); return r

def require_reviewer(authorization: str | None = Header(default=None)):
    err = auth.verify(authorization, config.reviewer_token())
    if err: raise HTTPException(err[0], err[1], headers={"WWW-Authenticate": "Bearer"} if err[0] == 401 else None)

@app.get("/api/v1/auth/check", dependencies=[Depends(require_reviewer)])
def auth_check(): return {"ok": True}

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
    if not f.exists(): return {"available": False, "hint": "Run: python scripts\\evaluate.py"}
    d = json.load(open(f)); ch = config.DATA / "metrics_challenge.json"
    d["challenge"] = json.load(open(ch)) if ch.exists() else None
    return d

@app.post("/api/v1/campaigns/review", dependencies=[Depends(require_reviewer)])
def review(req: ReviewRequest):
    try:
        return {"saved": True, "review": service.review(req.a, req.b, req.decision, req.note)}
    except LookupError as e: raise HTTPException(404, str(e))
    except ValueError as e: raise HTTPException(422, str(e))

@app.get("/api/v1/reviews", dependencies=[Depends(require_reviewer)])
def reviews(): return db.review_log()

@app.get("/api/v1/campaigns/{cid}/brief")
def brief(cid: str):
    for c in service.clusters()["clusters"]:
        if c["campaign_id"] == cid: return c["brief"]
    raise HTTPException(404, "Campaign not found")

@app.get("/api/v1/stats")
def stats(): return service.stats()

@app.delete("/api/v1/reports/{rid}", dependencies=[Depends(require_reviewer)])
def delete_report(rid: int):
    if db.delete_report(rid) == 0: raise HTTPException(404, "Report not found")
    return {"deleted": True}
