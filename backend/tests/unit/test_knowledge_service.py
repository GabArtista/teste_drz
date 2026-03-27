import pytest
from unittest.mock import AsyncMock
from app.Domain.Knowledge.Services.knowledge_service import KnowledgeService
from app.Domain.Knowledge.Entities.knowledge_base import KnowledgeBase
from app.Exceptions.domain_exceptions import NoKnowledgeBaseException


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.find_active_by_user = AsyncMock(return_value=None)
    repo.deactivate_all_by_user = AsyncMock(return_value=None)
    repo.create = AsyncMock(side_effect=lambda kb: kb)
    return repo


@pytest.fixture
def service(mock_repo):
    return KnowledgeService(mock_repo)


@pytest.mark.asyncio
async def test_upload_deactivates_previous(service, mock_repo):
    await service.upload("user1", "texto de teste")
    mock_repo.deactivate_all_by_user.assert_called_once_with("user1")


@pytest.mark.asyncio
async def test_upload_creates_kb(service, mock_repo):
    kb = await service.upload("user1", "  texto  ")
    assert kb.text == "texto"
    assert kb.char_count == 5
    assert kb.user_id == "user1"
    assert kb.is_active is True


@pytest.mark.asyncio
async def test_get_active_raises_when_none(service, mock_repo):
    with pytest.raises(NoKnowledgeBaseException):
        await service.get_active("user1")


@pytest.mark.asyncio
async def test_get_active_returns_kb(service, mock_repo):
    kb = KnowledgeBase("kb1", "user1", "texto", 5)
    mock_repo.find_active_by_user.return_value = kb
    result = await service.get_active("user1")
    assert result.id == "kb1"


@pytest.mark.asyncio
async def test_get_active_optional_returns_none(service, mock_repo):
    result = await service.get_active_optional("user1")
    assert result is None
