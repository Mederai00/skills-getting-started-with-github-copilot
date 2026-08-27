"""Tests for the FastAPI application using the Arrange-Act-Assert pattern."""


def test_root_redirect(client):
    # Arrange
    # (client fixture provides TestClient and isolated state)

    # Act
    resp = client.get("/", follow_redirects=False)

    # Assert
    assert resp.status_code == 307
    assert resp.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Programming Class"
    email = "duplicate@example.com"

    # Act
    first = client.post(f"/activities/{activity}/signup", params={"email": email})
    second = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json().get("detail") == "Student already signed up for this activity"


def test_signup_missing_activity(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "noone@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # existing participant in seed data

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_missing_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 404
