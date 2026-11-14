import json, sqlite3, time
from . import config

def conn():
    c = sqlite3.connect(config.DB_PATH); c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY, created REAL, text_fp TEXT UNIQUE,
      outcome TEXT, risk INTEGER, categories TEXT, text TEXT, indicators TEXT)""")
    c.execute("CREATE TABLE IF NOT EXISTS review_log(id INTEGER PRIMARY KEY, a INTEGER, b INTEGER, decision TEXT, note TEXT, ts REAL)")
    return c

def add_report(res, redacted, ind, text_fp, ts=None):
    """Returns new report id, or None if duplicate."""
    c = conn()
    try:
        cur = c.execute("INSERT INTO reports(created,text_fp,outcome,risk,categories,text,indicators) VALUES(?,?,?,?,?,?,?)",
                  (ts or time.time(), text_fp, res["outcome"], res["risk_score"], json.dumps(res["categories"]), redacted,
                   json.dumps([[k, f, l] for (k, f), l in ind.items()])))
        c.commit(); return cur.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        c.close()

def all_reports(limit=500):
    c = conn(); rows = c.execute("SELECT * FROM reports WHERE outcome='suspicious' ORDER BY id DESC LIMIT ?", (limit,)).fetchall(); c.close()
    return [{"id": r["id"], "text": r["text"], "ts": r["created"], "cats": set(json.loads(r["categories"])),
             "ind": {(k, f): l for k, f, l in json.loads(r["indicators"])}} for r in rows]

def report_exists(i):
    c = conn(); r = c.execute("SELECT 1 FROM reports WHERE id=?", (i,)).fetchone(); c.close(); return r is not None

def delete_report(i):
    c = conn(); n = c.execute("DELETE FROM reports WHERE id=?", (i,)).rowcount
    c.execute("DELETE FROM review_log WHERE a=? OR b=?", (i, i)); c.commit(); c.close(); return n

def add_review(a, b, decision, note):
    a, b = sorted((a, b)); c = conn(); ts = time.time()
    c.execute("INSERT INTO review_log(a,b,decision,note,ts) VALUES(?,?,?,?,?)", (a, b, decision, note, ts)); c.commit(); c.close()
    return {"a": a, "b": b, "decision": decision, "note": note, "ts": ts}

def latest_reviews():
    c = conn(); rows = c.execute("SELECT a,b,decision,note,ts FROM review_log ORDER BY id").fetchall(); c.close()
    out = {}
    for r in rows: out[(r["a"], r["b"])] = {"decision": r["decision"], "note": r["note"], "ts": r["ts"]}
    return out

def review_log(limit=100):
    c = conn(); rows = c.execute("SELECT a,b,decision,note,ts FROM review_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def purge_older_than(days):
    c = conn(); n = c.execute("DELETE FROM reports WHERE created < ?", (time.time() - days * 86400,)).rowcount; c.commit(); c.close(); return n
