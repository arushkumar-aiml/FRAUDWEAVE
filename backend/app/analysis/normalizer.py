import re, unicodedata
_ZW = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff\u00ad"), None)
# Cyrillic/Greek look-alikes -> Latin
_HOMO = {"а":"a","е":"e","о":"o","р":"p","с":"c","х":"x","у":"y","і":"i","ѕ":"s","ј":"j","ԁ":"d","ο":"o","α":"a","А":"A","В":"B","Е":"E","К":"K","М":"M","Н":"H","О":"O","Р":"P","С":"C","Т":"T","Х":"X","І":"I"}

def normalize(text: str) -> str:
    """NFKC, strip zero-width chars, map homoglyphs, collapse spaces. Case is kept so spans stay valid."""
    t = unicodedata.normalize("NFKC", text).translate(_ZW)
    t = "".join(_HOMO.get(c, c) for c in t)
    return re.sub(r"\s+", " ", t).strip()

def supported_script_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    ok = sum(1 for c in letters if c.isascii() or "\u0900" <= c <= "\u097f")
    return ok / len(letters)
