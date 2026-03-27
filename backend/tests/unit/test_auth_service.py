import pytest
from unittest.mock import AsyncMock, MagicMock
from app.Domain.User.Services.auth_service import AuthService
from app.Domain.User.Entities.user import User
from app.Exceptions.domain_exceptions import EmailAlreadyExistsException, InvalidCredentialsException


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.find_by_email = AsyncMock(return_value=None)
    repo.find_by_id = AsyncMock(return_value=None)
    repo.create = AsyncMock(side_effect=lambda u: u)
    return repo


@pytest.fixture
def auth_service(mock_repo):
    return AuthService(mock_repo)


@pytest.mark.asyncio
async def test_register_success(auth_service, mock_repo):
    user, token = await auth_service.register("João", "joao@test.com", "senha123")
    assert user.email == "joao@test.com"
    assert user.name == "João"
    assert token is not None
    assert len(token) > 10


@pytest.mark.asyncio
async def test_register_duplicate_email(auth_service, mock_repo):
    mock_repo.find_by_email.return_value = User("1", "João", "joao@test.com", "hash")
    with pytest.raises(EmailAlreadyExistsException):
        await auth_service.register("João", "joao@test.com", "senha123")


@pytest.mark.asyncio
async def test_login_invalid_credentials(auth_service, mock_repo):
    mock_repo.find_by_email.return_value = None
    with pytest.raises(InvalidCredentialsException):
        await auth_service.login("naoexiste@test.com", "senha123")


@pytest.mark.asyncio
async def test_login_wrong_password(auth_service, mock_repo):
    import bcrypt
    hashed = bcrypt.hashpw(b"correta", bcrypt.gensalt()).decode()
    mock_repo.find_by_email.return_value = User("1", "João", "joao@test.com", hashed)
    with pytest.raises(InvalidCredentialsException):
        await auth_service.login("joao@test.com", "errada")


@pytest.mark.asyncio
async def test_login_success(auth_service, mock_repo):
    import bcrypt
    hashed = bcrypt.hashpw(b"senha123", bcrypt.gensalt()).decode()
    mock_repo.find_by_email.return_value = User("1", "João", "joao@test.com", hashed)
    user, token = await auth_service.login("joao@test.com", "senha123")
    assert user.email == "joao@test.com"
    assert token is not None


def test_decode_invalid_token(auth_service):
    with pytest.raises(InvalidCredentialsException):
        auth_service.decode_token("token.invalido.aqui")
