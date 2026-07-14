def test_candidate_report(test_client, admin_token):
    response = test_client.get(
        "/reports/candidates",
        headers=admin_token
    )

    assert response.status_code == 200


def test_selected_candidates(test_client, admin_token):
    response = test_client.get(
        "/reports/selected",
        headers=admin_token
    )

    assert response.status_code == 200