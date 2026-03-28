import re
from openai import AsyncOpenAI
from app.Domain.Chat.Services.ai_service import AIServiceInterface

_SYSTEM = """Você é um assistente que responde perguntas com base APENAS no texto que o usuário fornecerá.

REGRAS OBRIGATÓRIAS — SIGA NESTA ORDEM:
1. Antes de responder, verifique se existe alguma RESTRIÇÃO ou PROIBIÇÃO relevante à pergunta.
2. Se houver restrição relacionada ao assunto perguntado, informe-a PRIMEIRO e com clareza.
3. Só então complemente com outras informações do texto, se pertinente.
4. Se a resposta não estiver no texto, responda exatamente: "Não sei com base nas informações fornecidas."
5. Nunca use conhecimento externo.
6. Responda em português brasileiro, de forma direta e objetiva."""

_RESTRICTION_KEYWORDS = [
    "proibido", "não destinado", "não é destinado", "não são destinados",
    "não permitido", "hipótese alguma", "exclusivamente", "vedado",
    "nunca", "não deve", "não pode", "não é para", "apenas",
]


def _extract_restrictions(text: str) -> list[str]:
    """Extrai frases que contêm proibições ou restrições explícitas."""
    sentences = re.split(r"(?<=[.!?])\s+|\n", text)
    found = []
    for s in sentences:
        s = s.strip()
        if s and any(kw in s.lower() for kw in _RESTRICTION_KEYWORDS):
            found.append(s)
    return found


class OllamaAIService(AIServiceInterface):
    """Serviço de IA usando Ollama local — gratuito, sem internet."""

    def __init__(self, model: str = "qwen2.5:1.5b"):
        self.client = AsyncOpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1",
        )
        self.model = model

    async def ask(self, question: str, knowledge_text: str) -> str:
        restrictions = _extract_restrictions(knowledge_text)
        restriction_block = ""
        if restrictions:
            items = "\n".join(f"• {r}" for r in restrictions)
            restriction_block = f"⚠️ RESTRIÇÕES E PROIBIÇÕES PRESENTES NO TEXTO:\n{items}\n\n"

        user_msg = f"""{restriction_block}TEXTO BASE COMPLETO:
---
{knowledge_text}
---

PERGUNTA: {question}"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=512,
            temperature=0.1,
        )
        return response.choices[0].message.content or "Não sei com base nas informações fornecidas."
