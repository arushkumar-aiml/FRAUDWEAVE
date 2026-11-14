# PROJECT_STATUS
## Done (sandbox-verified)
- Backend: normalizer, rules.json engine, offline URL analysis, classifier, decision, campaign link, SQLite reports, API.
- scripts/evaluate.py ran: 41 rows, grouped CV. Full pipeline P=1.0 R=0.739 FPR=0.0 abstain=0.171 (seed data, optimistic).
- Core tests (all except API) passed via a pytest-free runner: 0 failures.
## Added after ChatGPT review (sandbox-verified via pytest-free runner, 0 failures)
- Common-indicator downweighting, raw_total + evidence-score label, human accept/reject, Campaign Brief, rate limit, purge script.
## NOT verified
- tests/test_core.py::test_api (needs fastapi/pytest/httpx; sandbox had no network).
- Frontend never installed or built (no npm access). Expect small TypeScript fixes.
## Known issues
- ML model adds nothing over rules on the seed set (identical metrics). Needs a bigger dataset.
- 6/23 scams abstain (e.g. short Hinglish variants). Rules need more coverage.
## HANDOFF FOR CHATGPT
Review rule coverage, false-positive risks, link weights, privacy design, frontend code.
## HANDOFF FOR GEMINI
Need 100+ real-style Hindi/Hinglish scam samples and 50+ legitimate Indian bank/UPI/OTP messages, with sources and licences, no personal data.

## v3.0 (sandbox-verified via pytest-free runner: 0 failures)
Review workflow, complete-link merge, brief, stats, deletion, hard negatives, link families. Challenge set NOT yet collected.
NOT verified: pytest on API routes (needs fastapi), `npm run build`, running frontend against backend, rate-limit test, frontend tests (none written).
Skipped on purpose: Recharts/Lucide (extra dependencies), separate ARCHITECTURE/EVALUATION_REPORT/TEST_RESULTS files, user validation (no participants yet).

## v3.1: bare-domain redaction fix + reviewer token auth (logic tests pass in sandbox; API auth tests in tests/test_auth_api.py NOT run here, need pytest+fastapi). Frontend build still unverified.
