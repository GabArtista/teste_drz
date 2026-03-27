import pytest


@pytest.mark.asyncio
async def test_health(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_register(client):
    res = await client.post("/auth/register", json={
        "name": "Ana Silva",
        "email": "ana@test.com",
        "password": "senha123",
    })
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "ana@test.com"
    assert data["user"]["name"] == "Ana Silva"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"name": "Bob", "email": "bob@test.com", "password": "senha123"}
    await client.post("/auth/register", json=payload)
    res = await client.post("/auth/register", json=payload)
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/register", json={
        "name": "Carlos", "email": "carlos@test.com", "password": "senha123"
    })
    res = await client.post("/auth/login", json={
        "email": "carlos@test.com", "password": "senha123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/register", json={
        "name": "Diana", "email": "diana@test.com", "password": "correta"
    })
    res = await client.post("/auth/login", json={
        "email": "diana@test.com", "password": "errada"
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_me_authenticated(client):
    reg = await client.post("/auth/register", json={
        "name": "Eva", "email": "eva@test.com", "password": "senha123"
    })
    token = reg.json()["access_token"]
    res = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "eva@test.com"


@pytest.mark.asyncio
async def test_me_unauthenticated(client):
    res = await client.get("/auth/me")
    assert res.status_code == 403
