"""Insert synthetic demo reports (only if the database is empty)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from app.demo_data import seed
print("seeded", seed(), "reports")
