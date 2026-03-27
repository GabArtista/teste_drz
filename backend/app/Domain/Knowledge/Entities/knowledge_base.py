from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class KnowledgeBase:
    id: str
    user_id: str
    text: str
    char_count: int
    is_active: bool = True
    created_at: Optional[datetime] = None
