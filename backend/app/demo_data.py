"""Synthetic demo reports (reserved .test domains, invented UPI IDs). No real links or victims."""
import time
DEMO = [
 "Aapka KYC update nahi hua, account band ho jayega. Abhi verify karein http://sbi-kyc-help.test/login ya Rs 1 pay karein sbi.refund@okaxis",
 "SBI Alert: KYC pending, account will be blocked today. Verify at http://sbi-kyc-help.test/secure. Pay Rs 1 to sbi.refund@okaxis",
 "Your parcel is held at customs. Pay Rs 49 fee at http://parcel-retry.test to release",
 "Courier delivery failed! Parcel wapas ja raha hai. Rs 18 redelivery charge pay karein: http://parcel-retry.test/pay",
 "Part time job: like YouTube videos and earn Rs 5000 per day. Join Telegram group now",
]
def seed():
    from . import service, db
    c = db.conn(); n = c.execute("SELECT COUNT(*) FROM reports").fetchone()[0]; c.close()
    if n: return 0
    now = time.time(); done = 0
    for i, m in enumerate(DEMO):
        done += 1 if service.store_report(m, ts=now - i * 900).get("stored") else 0
    return done
