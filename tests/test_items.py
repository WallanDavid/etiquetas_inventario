import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_criar_listar_item():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Criar item
        response = await client.post("/items", json={
            "nome": "Produto Teste",
            "codigo": "TESTE123",
            "quantidade": 5
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Item cadastrado com sucesso"

        # Listar itens
        response = await client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert any(item["codigo"] == "TESTE123" for item in data)
