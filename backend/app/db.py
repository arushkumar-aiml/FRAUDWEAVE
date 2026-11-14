import json, sqlite3, time
from . import config

def conn():
    c = sqlite3.connect(config.DB_PATH); c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY, created REAL, text_fp TEXT UNIQUE,
      outcome TEXT, risk INTEGER, categories TEXT, text TEXT, indicators TEXT)""")
    c.execute("CREATE TABLE IF NOT EXISTS reviews(a INTEGER, b INTEGER, decision TEXT, PRIMARY KEY(a,b))")
    return c

def add_report(res: dict, redacted: str, ind: dict, text_fp: str, ts=None) -> bool:
    c = conn()
    try:
        c.execute("INSERT INTO reports(created,text_fp,outcome,risk,categories,text,indicators) VALUES(?,?,?,?,?,?,?)",
                  (ts or time.time(), text_fp, res["outcome"], res["risk_score"], json.dumps(res["categories"]), redacted,
                   json.dumps([[k, f, l] for (k, f), l in ind.items()])))
        c.commit(); return True
    except sqlite3.IntegrityError:
        return False  # duplicate
    finally:
        c.close()

def all_reports(limit=500):
    c = conn(); rows = c.execute("SELECT * FROM reports WHERE outcome='suspicious' ORDER BY created DESC LIMIT ?", (limit,)).fetchall(); c.close()
    return [{"id": r["id"], "text": r["text"], "ts": r["created"], "cats": set(json.loads(r["categories"])),
             "ind": {(k, f): l for k, f, l in json.loads(r["indicators"])}} for r in rows]

def set_review(a: int, b: int, decision: str):
    a, b = sorted((a, b)); c = conn()
    c.execute("INSERT OR REPLACE INTO reviews(a,b,decision) VALUES(?,?,?)", (a, b, decision)); c.commit(); c.close()

def reviews() -> dict:
    c = conn(); rows = c.execute("SELECT a,b,decision FROM reviews").fetchall(); c.close()
    return {(r["a"], r["b"]): r["decision"] for r in rows}

def purge_older_than(days: int) -> int:
    import time
    c = conn(); n = c.execute("DELETE FROM reports WHERE created < ?", (time.time() - days * 86400,)).rowcount; c.commit(); c.close(); return n
