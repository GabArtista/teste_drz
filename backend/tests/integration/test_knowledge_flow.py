import pytest


async def get_token(client, suffix=""):
    res = await client.post("/auth/register", json={
        "name": f"User{suffix}",
        "email": f"user{suffix}@test.com",
        "password": "senha123",
    })
    return res.json()["access_token"]


@pytest.mark.asyncio
async def test_upload_text(client):
    token = await get_token(client, "kn1")
    res = await client.post(
        "/knowledge/upload-text",
        json={"text": "Este é o texto de teste para conhecimento."},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["has_text"] is True
    assert data["char_count"] > 0
    assert "id" in data


@pytest.mark.asyncio
async def test_get_current_after_upload(client):
    token = await get_token(client, "kn2")
    await client.post(
        "/knowledge/upload-text",
        json={"text": "Texto importante para recuperar."},
        headers={"Authorization": f"Bearer {token}"},
    )
    res = await client.get("/knowledge/current", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["has_text"] is True


@pytest.mark.asyncio
async def test_get_current_without_upload(client):
    token = await get_token(client, "kn3")
    res = await client.get("/knowledge/current", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["has_text"] is False


@pytest.mark.asyncio
async def test_upload_replaces_previous(client):
    token = await get_token(client, "kn4")
    await client.post(
        "/knowledge/upload-text",
        json={"text": "Primeiro texto"},
        headers={"Authorization": f"Bearer {token}"},
    )
    await client.post(
        "/knowledge/upload-text",
        json={"text": "Segundo texto substituto"},
        headers={"Authorization": f"Bearer {token}"},
    )
    res = await client.get("/knowledge/current", headers={"Authorization": f"Bearer {token}"})
    assert "Segundo texto substituto" in res.json()["preview"]


@pytest.mark.asyncio
async def test_upload_requires_auth(client):
    res = await client.post("/knowledge/upload-text", json={"text": "texto"})
    assert res.status_code == 403
