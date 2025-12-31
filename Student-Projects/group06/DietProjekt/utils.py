import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

OUTPUT_DIR = Path("outputs")


def save_plan(plan: Dict[str, Any]) -> str:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"plan_{ts}.json"
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
