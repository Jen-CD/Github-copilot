import pytest
from fastapi.testclient import TestClient

def test_get_activities(client: TestClient):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

    # Check that each activity has the required fields
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)

def test_signup_for_activity(client: TestClient):
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_duplicate(client: TestClient):
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Try to signup again
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]

def test_signup_nonexistent_activity(client: TestClient):
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_from_activity(client: TestClient):
    # First signup
    client.post("/activities/Programming%20Class/signup?email=unregister@mergington.edu")

    # Then unregister
    response = client.post("/activities/Programming%20Class/unregister?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered unregister@mergington.edu from Programming Class" in data["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "unregister@mergington.edu" not in activities["Programming Class"]["participants"]

def test_unregister_not_signed_up(client: TestClient):
    response = client.post("/activities/Programming%20Class/unregister?email=notsignedup@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student is not signed up for this activity" in data["detail"]

def test_unregister_nonexistent_activity(client: TestClient):
    response = client.post("/activities/Nonexistent%20Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]