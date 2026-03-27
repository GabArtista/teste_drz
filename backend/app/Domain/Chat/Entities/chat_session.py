from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ChatSession:
    id: str
    user_id: str
    knowledge_base_id: str
    created_at: Optional[datetime] = None
