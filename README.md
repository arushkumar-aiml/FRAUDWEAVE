
# FraudWeave
### Explainable Scam Campaign Triage

**Detect Patterns. Connect Reports. Protect Communities.**

An India-focused cybersecurity prototype that helps cyber-awareness volunteers analyze suspicious messages, connect related scam reports, and generate evidence-based campaign briefs.

**Built for INNOVEX 2026 | PS05 – AI-Powered Cybersecurity**

---

## Project Links

| Resource | Link |
|---|---|
| Live Application | https://fraudweave-api.vercel.app |
| Backend API | https://fraudweave-api.onrender.com |
| Health Check | https://fraudweave-api.onrender.com/health |
| API Documentation | https://fraudweave-api.onrender.com/docs |
| GitHub Repository | https://github.com/arushkumar-aiml/FRAUDWEAVE |
| Demo Video | **[ADD DEMO VIDEO LINK HERE]** |

> **Note:** The backend runs on a free tier. After inactivity, the first request may take approximately 30–60 seconds to wake up.

---

## 1. The Problem

Online scams frequently reach people through SMS, messaging applications, suspicious links, fake payment requests, and impersonation messages.

A single suspicious message may appear harmless in isolation. However, similar messages reported by different people can reveal a larger scam campaign.

Community volunteers and college cyber-awareness groups need tools to:

- Examine suspicious messages and understand warning signs.
- Identify repeated indicators across multiple reports.
- Understand why reports may be related.
- Review campaign connections before accepting them.
- Prepare useful evidence summaries for awareness and reporting.

Traditional message-level detection alone does not provide this complete community-level picture.

## 2. Our Solution

**FraudWeave is an explainable scam campaign triage platform** designed for cyber-awareness volunteers and college cyber clubs in India.

It combines message analysis, privacy-conscious reporting, campaign correlation, and human review into one workflow.

### How It Works

1. **Analyze:** Submit a suspicious English, Hindi, or Hinglish message.
2. **Explain:** View the detection outcome, matched evidence, and triggered rules.
3. **Report:** Store a report only after explicit user consent.
4. **Connect:** Identify potentially related reports using shared indicators.
5. **Review:** Allow authorized human reviewers to accept, reject, or mark campaign links as insufficient evidence.
6. **Generate:** Create a Campaign Brief containing relevant evidence, a time range, and victim-awareness guidance.

FraudWeave is an early-triage and awareness tool. It does not replace law enforcement, financial institutions, or official cybercrime reporting systems.

---

## 3. Key Features

| Feature | Description |
|---|---|
| Multilingual Message Analysis | Analyzes English, Hindi, and Hinglish messages. |
| Hybrid Detection | Combines explainable rules with a TF-IDF and Logistic Regression model. |
| Evidence Highlighting | Displays matched text spans and triggered detection rules. |
| Offline URL Inspection | Inspects URLs without fetching or opening them. |
| Three Analysis Outcomes | Suspicious, Low Apparent Risk, and Unable to Verify. |
| Campaign Correlation | Connects reports using shared indicators such as domains, UPI IDs, phone numbers, and message templates. |
| Evidence-Based Linking | Text similarity alone cannot establish a strong campaign connection. |
| Safe Campaign Merging | Prevents merging when rejected or unsupported pairwise relationships conflict with the proposed group. |
| Human Review | Supports Accept, Reject, and Insufficient Evidence decisions, with reviewer notes and history. |
| Campaign Brief | Generates a structured summary with evidence, time range, and victim-awareness guidance. |
| Privacy-Conscious Reporting | Requires explicit consent and applies sensitive-data redaction. |
| Evaluation Dashboard | Displays evaluation results and project limitations. |

### Understanding the Outcomes

- **Suspicious:** The message contains evidence indicating potential scam activity.
- **Low Apparent Risk:** The system found limited suspicious evidence. This does not mean the message is safe.
- **Unable to Verify:** Available evidence is insufficient for a confident assessment.

FraudWeave's scores represent evidence strength, not calibrated probabilities.

---

## 4. What Makes FraudWeave Different?

FraudWeave focuses on combining practical capabilities for community-based scam awareness.

**1. Indian Scam Context**

Designed with indicators relevant to Indian scam reports, including UPI/payment identifiers and multilingual message patterns.

**2. Explainable Detection**

Instead of presenting only a prediction, the platform shows the evidence and rules behind an assessment.

**3. Community-Level Campaign Awareness**

Moves beyond analyzing isolated messages by identifying potentially related reports.

**4. Human-Controlled Decisions**

Campaign relationships are reviewed by authorized humans rather than being treated as automatically confirmed facts.

**5. Privacy-Conscious Correlation**

Uses redaction and HMAC-based indicator fingerprints to support correlation without relying on unrestricted storage of raw personal information.

**6. Transparent Uncertainty**

Includes an Unable to Verify outcome and explicitly communicates detection and evaluation limitations.

> Campaign correlation is an established area of cybersecurity research. FraudWeave's contribution is its combination of community-oriented triage, Indian scam indicators, multilingual analysis, privacy-conscious reporting, and human-reviewed campaign briefs.

---

## 5. System Workflow

```text
       Suspicious Message
               |
               v
       Message Normalization
               |
               v
       Hybrid Detection Engine
          /           \
         v             v
    Rule Engine     ML Model
         \             /
          v           v
       Evidence-Based Decision
               |
               v
         Analysis Result
               |
        Explicit Consent
               |
               v
       Redaction & Fingerprinting
               |
               v
        Campaign Correlation
               |
               v
          Human Review
        /      |       \
    Accept   Reject   Insufficient
        \      |       /
               v
         Campaign Brief
               |
               v
       Awareness & Reporting
```

---

## 6. Technology Stack

| Layer | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Database | SQLite |
| Machine Learning | scikit-learn |
| Text Representation | TF-IDF |
| Classification | Logistic Regression |
| Frontend | Next.js 14, TypeScript |
| Styling | Tailwind CSS |
| Validation & Testing | Pydantic, pytest |
| Privacy | Redaction, HMAC fingerprinting |
| Backend Hosting | Render |
| Frontend Hosting | Vercel |

No paid APIs are required for the core analysis workflow. URL inspection is performed offline without fetching submitted URLs.

---

## 7. Application Pages

| Route | Purpose |
|---|---|
| `/` | Dashboard with report statistics, categories, and review status |
| `/analyze` | Message analysis and evidence display |
| `/campaigns` | Campaign Intelligence and reviewer actions |
| `/campaigns/[id]` | Individual Campaign Brief |
| `/metrics` | Evaluation results and performance information |
| `/about` | Project information, privacy, and limitations |

---

## 8. Evaluation and Testing

FraudWeave has been tested across backend functionality, security-related workflows, and frontend production compilation.

### Engineering Verification

| Check | Result |
|---|---|
| Backend pytest suite | **53 tests passed** |
| Frontend production build | **Passed** |
| Frontend production routes | 8 |
| Backend health endpoint | Available on deployed service |

### Challenge-Set Evaluation

The project was evaluated on a separate 58-message challenge set.

| Metric | Result |
|---|---:|
| Precision | 0.93 |
| Recall | 0.48 |
| False Positive Rate | 0.03 |
| Abstention Rate | 0.21 |
| True Positives | 13 |
| False Positives | 1 |
| False Negatives | 14 |

**Evaluation Disclosure**

- The challenge set was AI-written by the same assistant that helped develop the detection rules.
- It was not an independently authored or independently validated benchmark.
- The rules were frozen before this challenge evaluation.
- These results are preliminary and must not be interpreted as real-world detection accuracy.
- No real-user validation study has been completed.

The results indicate a useful precision signal but also show that the system misses a significant number of scam-type messages. Improving recall and multilingual coverage remains important future work.

---

## 9. Privacy and Security

Privacy and responsible handling of submitted reports are important design considerations.

### Privacy Measures

- Reports are stored only after explicit consent.
- Stored message text undergoes sensitive-data redaction.
- Indicators are represented using HMAC fingerprints.
- HMAC fingerprints are pseudonymous, not anonymous.
- Trend categories with fewer than three reports are hidden.
- Reviewers can delete reports.

### Security Measures

- Reviewer-only endpoints require a bearer token configured through an environment variable.
- Reviewer token comparison uses constant-time comparison.
- Ten failed reviewer login attempts trigger a 15-minute IP lockout.
- Rate limits apply to selected analysis, linking, and reporting endpoints.
- Security headers are configured on the backend and frontend.
- Reviewer tokens are kept in browser session storage rather than embedded in the frontend build.

These are baseline protections for a prototype, not a claim of production-grade security.

---

## 10. Honest Limitations

FraudWeave is an early-stage prototype. Its limitations include:

1. The training dataset is small, handwritten, and synthetic.
2. Detection rules were tuned using the development dataset.
3. The 58-message challenge set was AI-written and not independently authored.
4. Recall is currently limited, especially for some emerging scam patterns and Hindi/Hinglish variations.
5. No independent human-written benchmark or real-user validation study has been completed.
6. Campaign-linking weights are heuristic and have not been validated in a real-world deployment.
7. URLs are inspected offline; the system does not perform live threat-intelligence lookups or bank/account verification.
8. Regex-based redaction can miss unusual formats.
9. Reviewer protection uses a single bearer token and is not production-grade authentication.
10. Rate limiting and reviewer lockout are in-memory and reset when the service restarts.
11. The frontend has no Content Security Policy configured.
12. Free-tier hosting introduces cold starts, and the SQLite database is not persistent across redeployments.

FraudWeave does not identify attackers, prove criminal activity, or guarantee that a message is safe.

---

## 11. Future Scope

Potential future improvements include:

- Building a larger, independently collected and human-annotated multilingual dataset.
- Improving recall for emerging scam patterns.
- Expanding Hindi and Hinglish detection coverage.
- Evaluating campaign correlation on real-world, consented reports.
- Conducting usability studies with cyber-awareness volunteers.
- Introducing persistent database infrastructure and stronger reviewer identity management.
- Adding independently maintained threat-intelligence integrations.
- Improving evaluation with independent benchmarks and broader testing.

---

## 12. Run Locally

### Prerequisites

- Python 3.11
- Node.js and npm
- Git

### Clone the Repository

```bash
git clone https://github.com/arushkumar-aiml/FRAUDWEAVE.git
cd FRAUDWEAVE
```

### Backend Setup (Windows PowerShell)

```powershell
cd backend

python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

pytest -v
python scripts\evaluate.py
python scripts\seed_demo.py

$env:FRAUDWEAVE_REVIEWER_TOKEN="choose-a-long-secret"

uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`

Health check: `http://localhost:8000/health`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

Open a second terminal:

```powershell
cd frontend

copy .env.local.example .env.local

npm install
npm run build
npm run dev
```

Frontend: `http://localhost:3000`

Configure `NEXT_PUBLIC_API` in `.env.local` to point to the local backend.

---

## 13. Environment Variables

### Backend

| Variable | Purpose |
|---|---|
| `FRAUDWEAVE_HMAC_KEY` | Secret key used for HMAC indicator fingerprints |
| `FRAUDWEAVE_REVIEWER_TOKEN` | Bearer token for reviewer-only endpoints |
| `FRAUDWEAVE_ORIGINS` | Allowed frontend origin |
| `FRAUDWEAVE_TRUST_PROXY` | Enables trusted proxy IP handling when configured appropriately |
| `FRAUDWEAVE_SEED_DEMO` | Enables demo-data seeding when the database is empty |
| `FRAUDWEAVE_DB` | Optional SQLite database path |
| `PYTHON_VERSION` | Python runtime version for Render |

### Frontend

| Variable | Purpose |
|---|---|
| `NEXT_PUBLIC_API` | Backend API base URL |

**Security Warning:** Never put secrets, reviewer tokens, or HMAC keys in `NEXT_PUBLIC_` variables or commit them to GitHub. Frontend public environment variables are visible to browser users.

---

## 14. Deployment

### Backend – Render

- Service type: Web Service
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`

### Frontend – Vercel

- Root directory: `frontend`
- Configure `NEXT_PUBLIC_API` with the deployed backend URL.
- Redeploy after changing build-time environment variables.

Configure `FRAUDWEAVE_ORIGINS` on Render to match the deployed frontend origin.

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 15. API Overview

| Method | Endpoint | Access |
|---|---|---|
| GET | `/health` | Public |
| POST | `/api/v1/analyze` | Public |
| POST | `/api/v1/reports` | Public, consent required |
| POST | `/api/v1/campaigns/link` | Public |
| GET | `/api/v1/campaigns` | Public |
| GET | `/api/v1/campaigns/{id}/brief` | Public |
| GET | `/api/v1/stats` | Public |
| GET | `/api/v1/metrics` | Public |
| GET | `/api/v1/auth/check` | Reviewer token |
| POST | `/api/v1/campaigns/review` | Reviewer token |
| GET | `/api/v1/reviews` | Reviewer token |
| DELETE | `/api/v1/reports/{id}` | Reviewer token |

Reviewer endpoints require:

```http
Authorization: Bearer <FRAUDWEAVE_REVIEWER_TOKEN>
```

The reviewer token must be configured on the backend. The Campaigns page provides a Reviewer Login interface.

---

## 16. Project Structure

```text
fraudweave/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── service.py
│   │   ├── demo_data.py
│   │   ├── analysis/
│   │   └── data/
│   ├── scripts/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── lib/
│   └── package.json
├── render.yaml
├── DEPLOYMENT.md
├── SECURITY_AND_PRIVACY.md
├── DATASET_CARD.md
└── USER_VALIDATION.md
```

---

## 17. Responsible Use

FraudWeave is intended for cybersecurity awareness, preliminary triage, and educational use.

- Do not treat automated results as proof of fraud.
- Do not assume that a low-apparent-risk result means a message is safe.
- Verify suspicious claims through official channels.
- Do not open suspicious links merely to test them.
- Do not use campaign links to accuse or identify individuals.
- Submit reports only with appropriate consent.
- Use official reporting channels for suspected cybercrime, including India's cybercrime portal at https://cybercrime.gov.in and helpline **1930**.

---

## 18. Team

**One Man Show**

**Arush Kumar**  
B.Tech CSE (AI/ML)  
Vision Institute of Technology

**Development:** Solo project developed with AI coding assistance. Problem selection, project scope, technical decisions, integration, testing, and deployment were handled by the team member.

---

## 19. Acknowledgment

FraudWeave was developed for INNOVEX 2026, Problem Statement PS05 – AI-Powered Cybersecurity, with the goal of exploring how explainable AI, privacy-conscious reporting, and human review can support community-level scam awareness.

**Detect Patterns. Connect Reports. Protect Communities.**

