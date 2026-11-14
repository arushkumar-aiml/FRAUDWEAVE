# 3-minute demo (synthetic data only; .test is a reserved, non-routable TLD)

1. (0:00) Hook: "Scam messages are judged one by one. FraudWeave asks: are these the SAME campaign, and what is the evidence?"
2. (0:20) Analyze, paste Hinglish scam:
   `Aapka KYC update nahi hua, account band ho jayega. Abhi verify karein http://sbi-kyc-help.test/login ya Rs 1 pay karein sbi.refund@okaxis`
   Show: Suspicious, highlighted evidence, link flags (never opened), actions (1930, cybercrime.gov.in).
3. (1:00) Paste the legitimate alert:
   `HDFC Bank: Rs 1,250.00 debited from a/c XX1234 on 14-Nov-26 at AMAZON. Not you? Call the number on your card.`
   Show: Low apparent risk (not "safe"). Say: "A bank name or a transaction is not a scam signal."
4. (1:30) Campaign Intelligence, compare A and B:
   A = the KYC message above. B = `SBI Alert: KYC pending, account will be blocked today. Verify at http://sbi-kyc-help.test/secure. Pay Rs 1 to sbi.refund@okaxis`
   Show: STRONG link: shared UPI ID + shared domain, with points per signal. Then compare A with
   `Your parcel is held at customs. Pay Rs 49 fee at http://parcel-retry.test to release` -> insufficient evidence.
5. (2:15) Open the Campaign Brief and a review action (Accept / Reject). Say: "Only strong links merge clusters, and a human can override."
6. (2:40) Metrics page: precision 1.0, recall 0.975, FPR 0, abstain 2% on 147 hand-written messages, tuned on the same set. "We state the limits."
Hard questions: novelty (campaign linking exists in VECTPHISH/PhishLumos; ours is Indian-language UPI-aware volunteer triage),
accuracy (small seed set, not real-world), privacy (redacted + HMAC, pseudonymous not anonymous), URLs (never fetched).
