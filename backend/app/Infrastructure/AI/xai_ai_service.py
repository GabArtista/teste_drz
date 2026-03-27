from pathlib import Path
from openai import AsyncOpenAI
from app.Domain.Chat.Services.ai_service import AIServiceInterface
from config.settings import settings

_PROMPT_PATH = Path(__file__).parent.parent.parent.parent / "resources" / "prompts" / "knowledge_qa.txt"

# Provider configs — troca só a chave no .env
_PROVIDERS = {
    "xai":  {"base_url": "https://api.x.ai/v1",              "key_env": "XAI_API_KEY",    "model": "grok-3-mini-fast"},
    "groq": {"base_url": "https://api.groq.com/openai/v1",   "key_env": "GROQ_API_KEY",   "model": "llama-3.3-70b-versatile"},
    "openai": {"base_url": "https://api.openai.com/v1",      "key_env": "OPENAI_API_KEY", "model": "gpt-4o-mini"},
}


class XAIService(AIServiceInterface):
    def __init__(self):
        provider = settings.AI_PROVIDER
        cfg = _PROVIDERS.get(provider, _PROVIDERS["xai"])

        key = getattr(settings, cfg["key_env"], "") or ""
        if not key:
            raise RuntimeError(f"Chave de API não configurada para provider '{provider}'. Defina {cfg['key_env']} no .env")

        self.client = AsyncOpenAI(api_key=key, base_url=cfg["base_url"])
        self.model = settings.AI_MODEL or cfg["model"]
        self._template = _PROMPT_PATH.read_text(encoding="utf-8")

    async def ask(self, question: str, knowledge_text: str) -> str:
        prompt = (
            self._template
            .replace("{knowledge_text}", knowledge_text)
            .replace("{question}", question)
        )
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        return response.choices[0].message.content or "Não sei com base nas informações fornecidas."
