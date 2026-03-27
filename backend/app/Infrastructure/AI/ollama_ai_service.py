from pathlib import Path
from openai import AsyncOpenAI
from app.Domain.Chat.Services.ai_service import AIServiceInterface

_SYSTEM = """Você é um assistente que responde perguntas com base APENAS no texto que o usuário fornecerá.

REGRAS OBRIGATÓRIAS:
- Responda SOMENTE com informações do texto fornecido.
- Se o texto mencionar proibições ou restrições, informe-as claramente.
- Se a resposta não estiver no texto, responda exatamente: "Não sei com base nas informações fornecidas."
- Nunca use conhecimento externo.
- Responda em português brasileiro, de forma direta e objetiva."""


class OllamaAIService(AIServiceInterface):
    """Serviço de IA usando Ollama local — gratuito, sem internet."""

    def __init__(self, model: str = "qwen2.5:1.5b"):
        self.client = AsyncOpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1",
        )
        self.model = model

    async def ask(self, question: str, knowledge_text: str) -> str:
        user_msg = f"""TEXTO BASE:
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
