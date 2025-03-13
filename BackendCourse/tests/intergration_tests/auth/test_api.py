import pytest


@pytest.mark.parametrize("login, password, status_code", [
    ("qwerty@mail.com", "qwerty", 200),
    ("tigerclaw@icloud.com", "tigerclaw123", 200),
    ("", 0000, 422),
    ("!@<>.()", "", 422)
])
async def test_register_user(login, password, status_code, ac):
    response = await ac.post(
        "/auth/register",
        json={
            "email": login,
            "password": password
        })
    assert response.status_code == status_code


@pytest.mark.parametrize("login, password, status_code", [
    ("qwerty@mail.com", "qwerty", 200),
    ("tigerclaw@icloud.com", "tigerclaw123", 200),
    ("pipiska@gmail.com", "sosiska321", 500),
    ("", 0000, 422)
])
async def test_auth_user_flow(login, password, status_code, ac):
    response = await ac.post(
        "/auth/login",
        json={
            "email": login,
            "password": password
        })

    assert response.status_code == status_code

    response = await ac.get("/auth/me")
    assert response.status_code == 200
    assert ac.cookies["access_token"]

    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == 200
