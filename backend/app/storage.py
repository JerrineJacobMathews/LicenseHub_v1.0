import json
from pathlib import Path
from typing import Any, Dict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_json(name: str) -> Dict[str, Any]:
    path = DATA_DIR / f"{name}.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
