def test_get_interviews(test_client, admin_token):
    response = test_client.get(
        "/interviews/",
        headers=admin_token
    )

    assert response.status_code == 200