"""Retention: delete reports older than N days (default 30). Usage: python scripts/purge.py 30"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from app import db
print("deleted", db.purge_older_than(int(sys.argv[1]) if len(sys.argv) > 1 else 30))
