from pathlib import Path
import anthropic
from app.Domain.Chat.Services.ai_service import AIServiceInterface
from config.settings import settings

_PROMPT_PATH = Path(__file__).parent.parent.parent.parent / "resources" / "prompts" / "knowledge_qa.txt"


class AnthropicAIService(AIServiceInterface):
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self._template = _PROMPT_PATH.read_text(encoding="utf-8")

    async def ask(self, question: str, knowledge_text: str) -> str:
        prompt = self._template.format(
            knowledge_text=knowledge_text,
            question=question,
        )
        response = await self.client.messages.create(
            model=settings.AI_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
