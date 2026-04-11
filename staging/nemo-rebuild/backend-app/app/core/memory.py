import json
from pathlib import Path
from threading import RLock
from typing import Any


class PersistentMemory:
    def __init__(self, filepath: str = "/home/ubuntu/.openclaw/workspace/staging/nemo-rebuild/backend-app/data/memory_store.json"):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()
        self._store = {}
        self._load()

    def _load(self) -> None:
        with self._lock:
            if self.filepath.exists():
                try:
                    self._store = json.loads(self.filepath.read_text())
                except Exception:
                    self._store = {}
            else:
                self._store = {}
                self._save()

    def _save(self) -> None:
        with self._lock:
            tmp_path = self.filepath.with_suffix(".tmp")
            tmp_path.write_text(json.dumps(self._store, indent=2, ensure_ascii=False))
            tmp_path.replace(self.filepath)

    def get(self, key: str) -> Any:
        with self._lock:
            return self._store.get(key)

    def set(self, key: str, value: Any) -> bool:
        with self._lock:
            self._store[key] = value
            self._save()
            return True

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                self._save()
                return True
            return False

    def keys(self):
        with self._lock:
            return list(self._store.keys())

    def append(self, key: str, value):
        with self._lock:
            existing = self._store.get(key)
            if not isinstance(existing, list):
                existing = []
            existing.append(value)
            self._store[key] = existing
            self._save()
            return True

    def all(self):
        with self._lock:
            return dict(self._store)


memory = PersistentMemory()
