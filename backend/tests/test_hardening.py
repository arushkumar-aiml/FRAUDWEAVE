"""Rate limits, lockout, proxy IP handling and security headers."""
import os, tempfile
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client(monkeypatch):
    from app import config, main
    monkeypatch.setattr(config, "DB_PATH", os.path.join(tempfile.mkdtemp(), "t.db"))
    monkeypatch.setenv("FRAUDWEAVE_REVIEWER_TOKEN", "test-token")
    monkeypatch.delenv("FRAUDWEAVE_TRUST_PROXY", raising=False)
    main._HITS.clear()
    yield TestClient(main.app)
    main._HITS.clear()

def test_security_headers_present(client):
    r = client.get("/health")
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["x-frame-options"] == "DENY"
    assert r.headers["referrer-policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in r.headers["content-security-policy"]

def test_docs_not_broken_by_csp(client):
    assert "content-security-policy" not in client.get("/docs").headers

def test_reviewer_lockout_after_failures(client):
    bad = {"Authorization": "Bearer wrong"}
    for _ in range(10):
        assert client.get("/api/v1/auth/check", headers=bad).status_code == 403
    assert client.get("/api/v1/auth/check", headers=bad).status_code == 429
    # lockout applies even to the correct token until the window passes
    assert client.get("/api/v1/auth/check", headers={"Authorization": "Bearer test-token"}).status_code == 429

def test_correct_token_never_counts_as_failure(client):
    ok = {"Authorization": "Bearer test-token"}
    for _ in range(15):
        assert client.get("/api/v1/auth/check", headers=ok).status_code == 200

def test_analyze_rate_limited(client):
    codes = [client.post("/api/v1/analyze", json={"text": "hello"}).status_code for _ in range(61)]
    assert codes[:60].count(200) == 60 and codes[60] == 429

def test_report_rate_limited(client):
    codes = [client.post("/api/v1/reports", json={"text": f"KYC update karo http://x{i}.top", "consent": False}).status_code for i in range(21)]
    assert codes[20] == 429

def test_proxy_header_ignored_unless_enabled(client):
    for i in range(60):
        client.post("/api/v1/analyze", json={"text": "hi"}, headers={"X-Forwarded-For": f"1.1.1.{i}"})
    assert client.post("/api/v1/analyze", json={"text": "hi"}, headers={"X-Forwarded-For": "9.9.9.9"}).status_code == 429

def test_proxy_header_used_when_enabled(client, monkeypatch):
    monkeypatch.setenv("FRAUDWEAVE_TRUST_PROXY", "1")
    for i in range(60):
        assert client.post("/api/v1/analyze", json={"text": "hi"}, headers={"X-Forwarded-For": "2.2.2.2"}).status_code == 200
    assert client.post("/api/v1/analyze", json={"text": "hi"}, headers={"X-Forwarded-For": "2.2.2.2"}).status_code == 429
    assert client.post("/api/v1/analyze", json={"text": "hi"}, headers={"X-Forwarded-For": "3.3.3.3"}).status_code == 200
