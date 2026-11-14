# Deployment (free tiers)

## 1. Push to GitHub
Make sure `.gitignore` is present. Never commit `backend/app/data/.hmac_key`, `*.db`, `.env.local`.
Run `python scripts\evaluate.py` in `backend` and commit `backend/app/data/metrics.json` so the Metrics page has data. Also commit `frontend/package-lock.json`.

## 2. Backend on Render (Web Service)
New > Blueprint (uses `render.yaml`) OR New > Web Service with:
- Root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Env vars: `PYTHON_VERSION=3.11.9`, `FRAUDWEAVE_HMAC_KEY=<long random secret>`, `FRAUDWEAVE_REVIEWER_TOKEN=<second long random secret>`, `FRAUDWEAVE_SEED_DEMO=1`,
  `FRAUDWEAVE_ORIGINS=https://<your-vercel-app>.vercel.app`
Check `https://<render-app>.onrender.com/health` returns {"status":"ok"}.
Free tier sleeps when idle (first request ~30-60 s) and SQLite data resets on redeploy: demo data is re-seeded at startup.

## 3. Frontend on Vercel
Import the repo, set Root Directory to `frontend`, add env var `NEXT_PUBLIC_API=https://<render-app>.onrender.com`, deploy.
Then put the Vercel URL into Render's `FRAUDWEAVE_ORIGINS` and redeploy the backend (CORS).

## 4. Before the demo
Open the live site 5 minutes earlier to wake the backend. Keep a recorded backup video.

## Privacy / retention
Reports store redacted text + HMAC fingerprints (pseudonymous, NOT anonymous). Delete old data with `python scripts\purge.py 30`.
Rate limit is in-memory per process, behind Render's proxy it keys on the proxy address: fine for a demo, not for production.

## Reviewer access
Accept/Reject, review log and report deletion need `Authorization: Bearer <FRAUDWEAVE_REVIEWER_TOKEN>`. Reading pages stay public (redacted data only).
The token is entered in the browser (kept in sessionStorage only) and is NOT part of the frontend build. Share it with judges only for the event, then rotate it.
If the token is not set the server returns 503 for those endpoints. This is basic bearer-token protection, not production-grade security.

## Persistence
Render free web services have no persistent disk: the SQLite file is lost on redeploy/restart-from-scratch. Demo data is re-seeded at startup. Persistent storage needs a paid disk or an external database (code change not done).
