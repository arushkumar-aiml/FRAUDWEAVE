"""URL handling is OFFLINE parsing only. Nothing here ever opens a socket."""
import ipaddress, json, re
from urllib.parse import urlparse
from ..config import DATA

URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"']+|\b(?:[a-z0-9-]+\.)+(?:com|in|net|org|co|xyz|top|info|online|site|link|ly|cc|club|vip|shop|me|test|tech|icu|buzz|click|work|support|live|store)\b(?:/[^\s<>\"']*)?", re.I)
SHORTENERS = {"bit.ly","tinyurl.com","t.ly","cutt.ly","is.gd","rb.gy","goo.gl","t.co","shorturl.at","rebrand.ly"}
BAD_TLDS = {"test","tech","co","xyz","top","club","vip","shop","cc","online","site","link","info","icu","buzz","click","work","support","live","store"}
OFFICIAL = {"sbi.co.in","onlinesbi.sbi","hdfcbank.com","icicibank.com","axisbank.com","paytm.com","npci.org.in","uidai.gov.in","cybercrime.gov.in","incometax.gov.in"}
BRANDS = ["sbi","hdfc","icici","axis","paytm","npci","uidai","kotak"]
SCAM_WORDS = ("kyc","refund","claim","reward","bonus","lottery","prize","winner","redeliver","redelivery","unfreeze","verify","bill-pay","billpay","fix-address","customs","clearance","fraud-cancel","limit-up","tasks","earn")
POINTS = {"scam_keywords":15,"shortener":20,"ip_host":30,"punycode":30,"suspicious_tld":15,"lookalike":35,"known_bad":100}

def _is_official(d: str) -> bool:
    return any(d == o or d.endswith("." + o) for o in OFFICIAL)

def known_bad() -> set:
    return set(json.load(open(DATA / "known_bad_domains.json"))["domains"])

def analyze_urls(text: str) -> list[dict]:
    bad, out, seen = known_bad(), [], set()
    for m in URL_RE.finditer(text):
        raw = m.group(0).rstrip(".,;:)")
        u = raw if "://" in raw else "http://" + raw
        try:
            host = (urlparse(u).hostname or "").lower()
        except ValueError:
            continue
        if not host or host in seen:
            continue
        seen.add(host)
        flags = []
        if host in SHORTENERS: flags.append("shortener")
        try:
            ipaddress.ip_address(host); flags.append("ip_host")
        except ValueError:
            pass
        if "xn--" in host: flags.append("punycode")
        if host.rsplit(".", 1)[-1] in BAD_TLDS: flags.append("suspicious_tld")
        if not _is_official(host) and any(b in host for b in BRANDS): flags.append("lookalike")
        if not _is_official(host) and any(w in host for w in SCAM_WORDS): flags.append("scam_keywords")
        if host in bad or any(host.endswith("." + b) for b in bad): flags.append("known_bad")
        out.append({"url": raw, "domain": host, "flags": flags, "trusted": _is_official(host)})
    return out
