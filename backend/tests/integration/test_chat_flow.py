import pytest
from unittest.mock import AsyncMock, patch


async def setup_user_with_knowledge(client, suffix=""):
    reg = await client.post("/auth/register", json={
        "name": f"ChatUser{suffix}",
        "email": f"chat{suffix}@test.com",
        "password": "senha123",
    })
    token = reg.json()["access_token"]
    await client.post(
        "/knowledge/upload-text",
        json={"text": "O elevador MC-70 suporta até 180 kg de carga máxima absoluta."},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token


@pytest.mark.asyncio
async def test_ask_without_knowledge(client):
    reg = await client.post("/auth/register", json={
        "name": "NoKnowledge", "email": "noknow@test.com", "password": "senha123"
    })
    token = reg.json()["access_token"]
    res = await client.post(
        "/chat/ask",
        json={"question": "Qual o peso máximo?"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_ask_requires_auth(client):
    res = await client.post("/chat/ask", json={"question": "Pergunta?"})
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_ask_creates_session(client):
    with patch(
        "app.Infrastructure.AI.anthropic_ai_service.AnthropicAIService.ask",
        new_callable=AsyncMock,
        return_value="O elevador suporta 180 kg.",
    ):
        token = await setup_user_with_knowledge(client, "c1")
        res = await client.post(
            "/chat/ask",
            json={"question": "Qual o peso máximo?"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        assert "session_id" in data
        assert data["answer"] == "O elevador suporta 180 kg."


@pytest.mark.asyncio
async def test_ask_reuses_session(client):
    with patch(
        "app.Infrastructure.AI.anthropic_ai_service.AnthropicAIService.ask",
        new_callable=AsyncMock,
        return_value="Resposta da IA.",
    ):
        token = await setup_user_with_knowledge(client, "c2")
        res1 = await client.post(
            "/chat/ask",
            json={"question": "Primeira pergunta"},
            headers={"Authorization": f"Bearer {token}"},
        )
        session_id = res1.json()["session_id"]

        res2 = await client.post(
            "/chat/ask",
            json={"question": "Segunda pergunta", "session_id": session_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res2.json()["session_id"] == session_id


@pytest.mark.asyncio
async def test_history_returns_messages(client):
    with patch(
        "app.Infrastructure.AI.anthropic_ai_service.AnthropicAIService.ask",
        new_callable=AsyncMock,
        return_value="Mensagem de resposta.",
    ):
        token = await setup_user_with_knowledge(client, "c3")
        ask_res = await client.post(
            "/chat/ask",
            json={"question": "Pergunta de teste"},
            headers={"Authorization": f"Bearer {token}"},
        )
        session_id = ask_res.json()["session_id"]

        hist_res = await client.get(
            f"/chat/history/{session_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert hist_res.status_code == 200
        messages = hist_res.json()["messages"]
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"
