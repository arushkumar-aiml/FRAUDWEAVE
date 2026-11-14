"""Needs fastapi/httpx (run with pytest on your PC)."""
import os, tempfile
from fastapi.testclient import TestClient

def _client(monkeypatch, token="test-token"):
    from app import config
    monkeypatch.setattr(config, "DB_PATH", os.path.join(tempfile.mkdtemp(), "t.db"))
    if token: monkeypatch.setenv("FRAUDWEAVE_REVIEWER_TOKEN", token)
    else: monkeypatch.delenv("FRAUDWEAVE_REVIEWER_TOKEN", raising=False)
    from app.main import app
    return TestClient(app)

BODY = {"a": 1, "b": 2, "decision": "accept"}

def test_review_needs_token(monkeypatch):
    c = _client(monkeypatch)
    assert c.post("/api/v1/campaigns/review", json=BODY).status_code == 401
    assert c.post("/api/v1/campaigns/review", json=BODY, headers={"Authorization": "Bearer nope"}).status_code == 403
    assert c.post("/api/v1/campaigns/review", json=BODY, headers={"Authorization": "Bearer test-token"}).status_code == 404  # authorized, reports don't exist

def test_delete_and_log_need_token(monkeypatch):
    c = _client(monkeypatch)
    assert c.delete("/api/v1/reports/1").status_code == 401
    assert c.get("/api/v1/reviews").status_code == 401
    assert c.delete("/api/v1/reports/1", headers={"Authorization": "Bearer test-token"}).status_code == 404
    assert c.get("/api/v1/auth/check", headers={"Authorization": "Bearer test-token"}).json() == {"ok": True}

def test_unconfigured_server_refuses(monkeypatch):
    c = _client(monkeypatch, token=None)
    assert c.post("/api/v1/campaigns/review", json=BODY, headers={"Authorization": "Bearer anything"}).status_code == 503

def test_public_read_endpoints_still_open(monkeypatch):
    c = _client(monkeypatch)
    for path in ("/health", "/api/v1/stats", "/api/v1/campaigns", "/api/v1/metrics"):
        assert c.get(path).status_code == 200
