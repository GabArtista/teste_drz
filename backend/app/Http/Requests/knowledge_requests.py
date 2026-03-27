from pydantic import BaseModel, field_validator


class UploadTextRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O texto não pode ser vazio.")
        return v
