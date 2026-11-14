# FraudWeave: Explainable Scam Campaign Triage (PS05)

Rule engine + TF-IDF/LogReg (English/Hindi/Hinglish), offline URL checks (never fetched), three outcomes
(suspicious / low apparent risk / unable to verify), and an **Explainable Campaign Link** that says why two
messages are linked, with which evidence, or that evidence is insufficient.

## Run (Windows PowerShell)
```
cd fraudweave\backend
python -m venv ..\.venv; ..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
python scripts\evaluate.py
python scripts\seed_demo.py
uvicorn app.main:app --reload
# new terminal
cd ..\frontend; copy .env.local.example .env.local; npm install; npm run dev
```
Open http://localhost:3000.

## Positioning
A community-powered, explainable scam campaign triage tool for cyber-awareness volunteers and college cyber clubs in India.
Campaign correlation itself is NOT novel (see VECTPHISH, PhishLumos, MISP, I4C Samanvaya). FraudWeave's contribution is
adapting evidence-based triage to community-reported Indian scams: UPI/VPA indicators, Hindi/Hinglish, privacy-preserving
reports, human review of links, and a victim-oriented Campaign Brief. It is an early-triage layer, not a law-enforcement tool.

## Safeguards
Indicators seen in >3 reports are downweighted; only strong links merge clusters; reviewers can accept/reject links;
report endpoint is rate-limited (20/hour/IP, in-memory); `python scripts\purge.py 30` deletes reports older than 30 days.
Scores are an *evidence score* (capped at 1.0), never a probability.

## Honest limits
- Dataset is a small hand-written/synthetic set (see metrics.json for exact counts). Rules were tuned on it, so metrics are NOT evidence of real-world accuracy. Independent challenge-set evaluation has not yet been completed.
- Link weights are unvalidated heuristics. Text similarity alone can never produce a "strong" link.
- No URL is ever fetched; unknown URLs are never marked safe. No bank/account verification.
- Stored reports keep only redacted text + HMAC fingerprints. Set FRAUDWEAVE_HMAC_KEY in production.
- Not yet done: deployment config, URLhaus/PhishTank feeds (needs a vetted offline snapshot), key rotation.

## Deployment
See DEPLOYMENT.md (Render + Vercel) and DEMO_SCRIPT.md. Env vars: FRAUDWEAVE_HMAC_KEY, FRAUDWEAVE_ORIGINS, FRAUDWEAVE_SEED_DEMO.
Seed demo data locally: `python scripts\seed_demo.py`.

## Reviewer access
Set `FRAUDWEAVE_REVIEWER_TOKEN` (PowerShell: `$env:FRAUDWEAVE_REVIEWER_TOKEN="your-secret"` before `uvicorn`). Review/delete endpoints need it; the Campaigns page has a Reviewer login box.
