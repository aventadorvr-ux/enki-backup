# Base Agent Class
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/agents/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.core.memory import memory
import structlog

logger = structlog.get_logger()

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.memory_key = f"agent:{agent_id}"
        self.logger = logger.bind(agent=agent_id)
    
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def store_state(self, state: Dict[str, Any]):
        memory.set(self.memory_key, state)
    
    def get_state(self) -> Dict[str, Any]:
        return memory.get(self.memory_key) or {}
    
    def log_action(self, action: str, details: Dict = None):
        self.logger.info(f"Agent action: {action}", details=details or {})
