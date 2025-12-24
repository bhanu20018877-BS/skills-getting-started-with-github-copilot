from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "tester@example.com"

    # Ensure participant not already present
    res = client.get("/activities")
    assert res.status_code == 200
    assert email not in res.json()[activity]["participants"]

    # Sign up
    signup_path = f"/activities/{quote(activity)}/signup?email={quote(email)}"
    res = client.post(signup_path)
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Confirm participant was added
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # Signing up again should fail
    res = client.post(signup_path)
    assert res.status_code == 400

    # Unregister
    unregister_path = f"/activities/{quote(activity)}/unregister?email={quote(email)}"
    res = client.post(unregister_path)
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Confirm participant was removed
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]


def test_unregister_nonexistent():
    activity = "Chess Club"
    email = "no-such@example.com"
    unregister_path = f"/activities/{quote(activity)}/unregister?email={quote(email)}"
    res = client.post(unregister_path)
    assert res.status_code == 400
