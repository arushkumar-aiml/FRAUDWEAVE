import os, secrets
from pathlib import Path
BASE = Path(__file__).parent
DATA = BASE / "data"
DB_PATH = os.environ.get("FRAUDWEAVE_DB", str(BASE.parent / "fraudweave.db"))
ALLOWED_ORIGINS = ["http://localhost:3000"]
MAX_TEXT = 2000
MIN_CATEGORY_COUNT = 3  # trends hide categories with fewer reports

def hmac_key() -> bytes:
    env = os.environ.get("FRAUDWEAVE_HMAC_KEY")
    if env:
        return env.encode()
    f = DATA / ".hmac_key"  # gitignored, generated locally on first run
    if not f.exists():
        f.write_text(secrets.token_hex(32))
    return f.read_text().strip().encode()
