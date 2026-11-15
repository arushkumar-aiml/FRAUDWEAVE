# FraudWeave: Explainable Scam Campaign Triage

**Detect Patterns. Connect Reports. Protect Communities.**

Built for INNOVEX 2026, Problem Statement PS05 (AI-Powered Cybersecurity).

| | |
|---|---|
| Live app (frontend) | https://fraudweave-api.vercel.app |
| Live API (backend) | https://fraudweave-api.onrender.com |
| Health check | https://fraudweave-api.onrender.com/health |
| API docs (Swagger) | https://fraudweave-api.onrender.com/docs |

> The backend runs on a free tier. If it has been idle, the first request can take 30-60 seconds to wake up.

---

## 1. What is FraudWeave?

FraudWeave is a community-powered triage tool for cyber-awareness volunteers and college cyber clubs in India.
It does three things:

1. **Analyzes** a suspicious message (English, Hindi, Hinglish) and explains *why* it looks suspicious, with the exact matched evidence.
2. **Connects** consented, redacted reports into possible scam campaigns, and says *why* two reports are linked (or that the evidence is insufficient).
3. **Generates a Campaign Brief** that volunteers can copy or print: evidence, time range, victim advice, and pointers to 1930 and cybercrime.gov.in. Nothing is auto-submitted.

It is an early-triage layer. It is **not** a law-enforcement tool and does **not** attribute attacks to anyone.

## 2. Features

| Area | What it does |
|---|---|
| Message analysis | Rule engine (`rules.json`) plus a TF-IDF + Logistic Regression model. Three outcomes: **Suspicious**, **Low apparent risk**, **Unable to verify**. |
| Explainability | Highlights exact matched spans and lists the rules that fired. |
| URL inspection | Offline only. URLs are never fetched. Unknown URLs are never marked "safe". |
| Campaign linking | Links reports by shared indicators (links, UPI IDs, phone numbers, templates). Text similarity alone can never create a strong link. |
| Safe merging | Two groups merge only if no pair between them is rejected or unsupported. A weak chain (A-B strong, B-C strong, A-C unrelated) does not merge. |
| Human review | Reviewers accept, reject, or mark "insufficient evidence", with notes and a history log. Rejected links stay visible. |
| Campaign Brief | Time range, evidence breakdown, templates, victim advice, copy and print. |
| Privacy | Consent required to store. Text is redacted. Indicators stored as HMAC fingerprints (pseudonymous, **not** anonymous). Categories with fewer than 3 reports are hidden from trends. |
| Evaluation | `scripts/evaluate.py` reports rules-only, ML-only and combined results, with a challenge-set mode. |

## 3. Pages

| Route | Purpose |
|---|---|
| `/` | Dashboard: report counts, categories, review status |
| `/analyze` | Paste a message and see the analysis |
| `/campaigns` | Linked campaigns, review actions, Reviewer login |
| `/campaigns/[id]` | Campaign Brief |
| `/metrics` | Evaluation results (loaded from `metrics.json`) |
| `/about` | Limitations and privacy notes |

## 4. Tech stack

- **Backend:** FastAPI, SQLite, scikit-learn, pydantic
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Hosting:** Render (backend), Vercel (frontend)
- No paid APIs. No external network calls at analysis time.

## 5. Project structure

```
fraudweave/
├── backend/
│   ├── app/
│   │   ├── main.py            # API routes, CORS, startup seeding
│   │   ├── auth.py            # Reviewer bearer-token check
│   │   ├── config.py          # Environment configuration
│   │   ├── db.py, service.py  # SQLite storage and business logic
│   │   ├── demo_data.py       # Synthetic demo reports
│   │   ├── analysis/          # normalizer, rules, urls, classifier, decision, campaign, pipeline
│   │   └── data/              # dataset.csv, rules.json, metrics.json, challenge_template.csv
│   ├── scripts/               # evaluate.py, seed_demo.py, purge.py
│   ├── tests/                 # test_core.py, test_auth_api.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/                   # Pages (Next.js app router)
│   ├── lib/                   # API client and types
│   └── package.json, package-lock.json
├── render.yaml                # Optional Render blueprint
├── DEPLOYMENT.md
├── SECURITY_AND_PRIVACY.md
├── DATASET_CARD.md
└── USER_VALIDATION.md
```

## 6. Run locally (Windows PowerShell)

### Backend
```powershell
cd fraudweave\backend
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
python scripts\evaluate.py
python scripts\seed_demo.py
$env:FRAUDWEAVE_REVIEWER_TOKEN="choose-a-long-secret"
uvicorn app.main:app --reload
```
Check http://localhost:8000/health. It should return `{"status":"ok"}`.

### Frontend (second terminal)
```powershell
cd fraudweave\frontend
copy .env.local.example .env.local
npm install
npm run build
npm run dev
```
Open http://localhost:3000.

## 7. Environment variables

### Backend (Render)

| Variable | Required | Meaning |
|---|---|---|
| `FRAUDWEAVE_HMAC_KEY` | Yes (production) | Long random secret used to fingerprint indicators |
| `FRAUDWEAVE_REVIEWER_TOKEN` | Yes | Secret for review and delete endpoints. If unset, those endpoints return 503. |
| `FRAUDWEAVE_ORIGINS` | Yes | Allowed frontend origin, e.g. `https://fraudweave-api.vercel.app` (no trailing slash) |
| `FRAUDWEAVE_TRUST_PROXY` | Recommended on Render | `1` makes rate limits use the client IP from `X-Forwarded-For` |
| `FRAUDWEAVE_SEED_DEMO` | Optional | `1` re-seeds 5 synthetic demo reports at startup when the database is empty |
| `FRAUDWEAVE_DB` | Optional | Path to the SQLite file |
| `PYTHON_VERSION` | Render | `3.11.9` |

### Frontend (Vercel)

| Variable | Meaning |
|---|---|
| `NEXT_PUBLIC_API` | Backend URL, e.g. `https://fraudweave-api.onrender.com` (no trailing slash) |

`NEXT_PUBLIC_` values are baked in at build time and are visible in the browser. **Never put secrets there.** After changing it on Vercel, you must redeploy.

## 8. Deployment summary

Full steps are in [DEPLOYMENT.md](DEPLOYMENT.md).

**Backend on Render (Web Service, Free instance)**
- Root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

**Frontend on Vercel**
- Root directory: `frontend`
- Env var: `NEXT_PUBLIC_API`

**CORS:** set `FRAUDWEAVE_ORIGINS` on Render to the Vercel URL, then redeploy the backend.

**Free-tier limits:** the backend sleeps when idle, and the SQLite file is lost on redeploy. Demo data is re-seeded at startup.

## 9. API overview

| Method | Endpoint | Access |
|---|---|---|
| GET | `/health` | Public |
| POST | `/api/v1/analyze` | Public |
| POST | `/api/v1/reports` | Public. Needs `consent: true`. Rate-limited to 20/hour/IP. |
| POST | `/api/v1/campaigns/link` | Public |
| GET | `/api/v1/campaigns` | Public |
| GET | `/api/v1/campaigns/{id}/brief` | Public |
| GET | `/api/v1/stats` | Public |
| GET | `/api/v1/metrics` | Public |
| GET | `/api/v1/auth/check` | Reviewer token |
| POST | `/api/v1/campaigns/review` | Reviewer token |
| GET | `/api/v1/reviews` | Reviewer token |
| DELETE | `/api/v1/reports/{id}` | Reviewer token |

Reviewer endpoints need the header `Authorization: Bearer <FRAUDWEAVE_REVIEWER_TOKEN>`.
They return 401 (missing), 403 (wrong token) or 503 (server has no token configured).
The Campaigns page has a **Reviewer login** box. The token is kept in `sessionStorage` only, never in the frontend build.

## 10. Testing

| Check | Command | Last result |
|---|---|---|
| Backend tests | `cd backend` then `pytest -v` | 53 passed (run on the submitted code) |
| Frontend build | `cd frontend` then `npm run build` | Passed, 8 routes |
| Evaluation | `python scripts\evaluate.py` | Writes `backend/app/data/metrics.json` |

Not covered: there are no frontend tests, and the in-memory rate limiter is not tested under a real proxy.

## 11. Evaluation

Exact dataset size, class balance and metrics are generated into `backend/app/data/metrics.json` and shown on the `/metrics` page. Nothing is hardcoded in the frontend.

Challenge-set mode (for a frozen, independent test):
```powershell
python scripts\evaluate.py --challenge app\data\challenge_template.csv
```

## 12. Honest limitations

- The dataset is small, hand-written and synthetic. The rules were tuned on it, so the metrics are **not** evidence of real-world accuracy.
- **An independent challenge-set evaluation has not been completed.** No user-validation study has been run.
- Link weights are unvalidated heuristics. Scores are evidence scores, never probabilities.
- URLs are never fetched. There is no bank or account verification and no live threat-intelligence feed.
- HMAC fingerprints are pseudonymous, not anonymous. Redaction is regex-based and can miss unusual formats.
- Reviewer protection is a single bearer token. It is basic protection, not production-grade security.
- Rate limiting and the reviewer lockout (10 failed logins per 15 min) are in-memory and per process; they reset on restart. No CSP on the frontend.
- Free hosting means cold starts and non-persistent storage.
- Campaign correlation itself is not novel (see VECTPHISH, PhishLumos, MISP, I4C Samanvaya). FraudWeave's contribution is adapting evidence-based triage to community-reported Indian scams: UPI indicators, Hindi/Hinglish, privacy-preserving reports, human review of links, and a victim-oriented brief.

## 13. Privacy and data retention

- Reports are stored only with explicit consent.
- Stored data is redacted text plus HMAC fingerprints.
- Reports can be deleted by a reviewer. Old data can be purged with `python scripts\purge.py 30`.
- Details: [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) and [DATASET_CARD.md](DATASET_CARD.md).

## 14. Team

Arush Kumar (solo submission).
