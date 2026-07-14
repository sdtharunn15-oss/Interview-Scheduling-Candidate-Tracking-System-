def test_register(test_client):
    response = test_client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@test.com",
            "password": "Admin123",
            "role": "Admin"
        }
    )

    assert response.status_code in [200, 201]


def test_login(test_client):
    response = test_client.post(
        "/auth/login",
        data={
            "username": "admin@test.com",
            "password": "Admin123"
        }
    )

    assert response.status_code == 200