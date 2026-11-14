"""Inserts demo reports so the Campaign screen has data. Uses the same service code as the API."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from app import service
now = time.time()
MSGS = [
 "Aapka KYC update nahi hua, account band ho jayega. Abhi verify karein http://sbi-kyc-update.xyz/login",
 "SBI Alert: KYC pending, account will be blocked today. Verify at http://sbi-kyc-update.xyz/secure",
 "Your refund is ready. Pay Rs 1 to verify: send to helpdesk123@ybl and share the OTP",
 "Refund pending: transfer Rs 1 to helpdesk123@ybl and enter UPI PIN to receive money",
 "Bijli connection aaj raat cut ho jayega. Turant bill update karein: http://bses-pay-now.top",
 "Part time job: like YouTube videos and earn Rs 5000 per day. Join Telegram group now",
]
for i, m in enumerate(MSGS):
    print(service.store_report(m, ts=now - i * 600))
