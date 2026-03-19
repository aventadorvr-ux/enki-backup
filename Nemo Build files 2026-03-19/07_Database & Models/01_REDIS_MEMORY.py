# Shared Memory - Redis Implementation
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/core/memory.py
# Status: FALLBACK TO LOCAL DICT (Redis not installed)

import json
from typing import Any, Optional
from app.core.config import get_settings

settings = get_settings()

class SharedMemory:
    def __init__(self):
        self._local = {}
        try:
            import redis
            self._redis = redis.from_url(settings.REDIS_URL)
            self._redis.ping()
        except:
            # ⚠️ Redis not available - using local dict (data lost on restart)
            self._redis = None
    
    def get(self, key: str) -> Optional[Any]:
        if self._redis:
            val = self._redis.get(key)
            return json.loads(val) if val else None
        return self._local.get(key)
    
    def set(self, key: str, value: Any, expire: int = None):
        data = json.dumps(value)
        if self._redis:
            self._redis.set(key, data, ex=expire)
        else:
            self._local[key] = value

memory = SharedMemory()

# ⚠️ ACTION REQUIRED:
# sudo apt install redis-server
# sudo systemctl enable redis
# sudo systemctl start redis
