from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional


@dataclass
class Message:
    id: str
    session_id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: Optional[datetime] = None
