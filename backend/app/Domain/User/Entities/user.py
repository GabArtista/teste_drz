from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    created_at: Optional[datetime] = None
