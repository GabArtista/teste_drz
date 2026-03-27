from pydantic import BaseModel, field_validator
from typing import Optional


class AskRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

    @field_validator("question")
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("A pergunta não pode ser vazia.")
        return v.strip()
