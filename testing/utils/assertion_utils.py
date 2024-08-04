
def assert_response(response, expected_status, expected_output):
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
    assert response.json() == expected_output, f"Expected output {expected_output}, got {response.json()}"