def test_feedback_not_found(test_client, admin_token):
    response = test_client.get(
        "/feedback/100",
        headers=admin_token
    )

    assert response.status_code in [404, 400]