import json
import time
from pathlib import Path

import requests

QUEUE_DIR = Path.home() / ".openclaw" / "workspace" / "queue"
LOG_DIR = Path.home() / ".openclaw" / "workspace" / "logs" / "runner"
API_BASE = "http://127.0.0.1:8000/api/v1/agents"

def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_DIR / "runner.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def process_task(file_path: Path) -> None:
    try:
        task = json.loads(file_path.read_text(encoding="utf-8"))

        agent = task["agent"]
        payload = task["payload"]
        output_path = Path(task["output_path"])

        log(f"Processing {file_path.name} -> {agent}")

        r = requests.post(
            f"{API_BASE}/{agent}/process",
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
        result = r.json()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

        log(f"SUCCESS -> {output_path}")

    except Exception as e:
        log(f"ERROR -> {file_path.name} -> {e}")

    finally:
        file_path.unlink(missing_ok=True)

def run() -> None:
    log("Agent runner started")
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        tasks = sorted(QUEUE_DIR.glob("*.json"))
        if not tasks:
            time.sleep(2)
            continue

        for task_file in tasks:
            process_task(task_file)

if __name__ == "__main__":
    run()
