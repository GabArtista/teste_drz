import pytest
from unittest.mock import AsyncMock, MagicMock
from app.Domain.Chat.Services.chat_service import ChatService
from app.Domain.Chat.Entities.chat_session import ChatSession
from app.Domain.Chat.Entities.message import Message
from app.Domain.Knowledge.Entities.knowledge_base import KnowledgeBase


def make_services(answer="Resposta da IA", kb_text="texto base", session=None):
    ai = AsyncMock()
    ai.ask = AsyncMock(return_value=answer)

    knowledge_svc = AsyncMock()
    knowledge_svc.get_active = AsyncMock(
        return_value=KnowledgeBase("kb1", "user1", kb_text, len(kb_text))
    )

    chat_repo = AsyncMock()
    chat_repo.find_session_by_id = AsyncMock(return_value=session)
    new_session = ChatSession("sess1", "user1", "kb1")
    chat_repo.create_session = AsyncMock(return_value=new_session)
    chat_repo.add_message = AsyncMock(side_effect=lambda m: m)
    chat_repo.get_messages = AsyncMock(return_value=[])

    return ChatService(ai, knowledge_svc, chat_repo), ai, knowledge_svc, chat_repo


@pytest.mark.asyncio
async def test_ask_creates_session_when_none():
    service, ai, _, chat_repo = make_services()
    result = await service.ask("user1", "Qual o peso máximo?")
    chat_repo.create_session.assert_called_once()
    assert result["answer"] == "Resposta da IA"
    assert result["session_id"] == "sess1"


@pytest.mark.asyncio
async def test_ask_reuses_existing_session():
    existing = ChatSession("existing_sess", "user1", "kb1")
    service, _, _, chat_repo = make_services(session=existing)
    result = await service.ask("user1", "Pergunta?", session_id="existing_sess")
    chat_repo.create_session.assert_not_called()
    assert result["session_id"] == "existing_sess"


@pytest.mark.asyncio
async def test_ask_saves_both_messages():
    service, _, _, chat_repo = make_services()
    await service.ask("user1", "Pergunta?")
    assert chat_repo.add_message.call_count == 2
    calls = chat_repo.add_message.call_args_list
    assert calls[0][0][0].role == "user"
    assert calls[1][0][0].role == "assistant"


@pytest.mark.asyncio
async def test_sources_found_false_when_not_in_text():
    service, _, _, _ = make_services(answer="Não sei com base nas informações fornecidas.")
    result = await service.ask("user1", "Pergunta impossível?")
    assert result["sources_found"] is False


@pytest.mark.asyncio
async def test_sources_found_true_when_answered():
    service, _, _, _ = make_services(answer="A capacidade é 120 kg.")
    result = await service.ask("user1", "Qual a capacidade?")
    assert result["sources_found"] is True
