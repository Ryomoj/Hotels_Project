import pytest


@pytest.mark.parametrize("login, password, status_code", [
    ("qwerty@mail.com", "qwerty", 200),
    ("qwerty@mail.com", "qwerty", 400),
    ("tigerclaw@icloud.com", "tigerclaw123", 200),
    ("abcde", "4321", 422),
    ("abcde@ef", "1234", 422),
])
async def test_auth_flow(login: str, password: str, status_code, ac):
    # /register
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": login,
            "password": password
        }
    )
    assert response_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": login,
            "password": password
        }
    )
    assert response_login.status_code == status_code
    assert ac.cookies["access_token"]
    assert "access_token" in response_login.json()

    # /me
    response_me = await ac.get("/auth/me")
    assert response_me.status_code == status_code
    user = response_me.json()
    assert user["email"] == login
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code
    assert "access_token" not in ac.cookies
