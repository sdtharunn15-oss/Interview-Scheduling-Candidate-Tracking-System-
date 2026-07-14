def test_create_candidate(test_client, admin_token):
    response = test_client.post(
        "/candidates/",
        headers=admin_token,
        json={
            "name": "John",
            "email": "john@test.com",
            "phone": "9876543210",
            "experience": 3,
            "skill_set": "Python",
            "application_status": "Applied"
        }
    )

    assert response.status_code == 201


def test_get_candidates(test_client, admin_token):
    response = test_client.get(
        "/candidates/",
        headers=admin_token
    )

    assert response.status_code == 200