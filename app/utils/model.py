import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "churn_model.joblib"

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Churn model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)