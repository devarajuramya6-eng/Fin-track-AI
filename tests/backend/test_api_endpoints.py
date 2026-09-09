import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_auth_registration_and_login_flow(client: AsyncClient):
    # Register a new user
    register_payload = {
        "email": "test.user@example.com",
        "password": "SuperSecretPassword123!",
        "full_name": "Test User",
        "preferred_currency": "USD",
    }
    reg_res = await client.post("/api/v1/auth/register", json=register_payload)
    assert reg_res.status_code in [201, 400]

    # Login with OAuth2 form data
    login_data = {
        "username": "test.user@example.com",
        "password": "SuperSecretPassword123!",
    }
    login_res = await client.post("/api/v1/auth/login", data=login_data)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
