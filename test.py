# test.py
import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    # make sure each test starts logged_out
    app.config['LOGGED_IN'] = False
    with app.test_client() as client:
        yield client


def test_read_main(client):
    """
    Test the root endpoint returns 200 and correct structure.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "1.0.0"}


def test_addition_logic(client):
    """
    Test the math endpoint to ensure logic holds.
    """
    response = client.get("/add/5/10")
    assert response.status_code == 200
    assert response.get_json() == {"result": 15}


def test_invalid_input(client):
    """
    Test that sending text instead of integers results in 404 (Flask behavior).
    """
    response = client.get("/add/five/ten")
    assert response.status_code == 404


# ---------- NEW TESTS FOR LOGIN & SUBTRACT ----------

def test_login_valid_account(client):
    """
    Login should succeed with a valid username/password.
    """
    response = client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "login successful"


def test_login_invalid_account(client):
    """
    Login should fail with wrong credentials.
    """
    response = client.post("/login", json={
        "username": "admin",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.get_json()["message"] == "invalid credentials"


def test_subtract_requires_login(client):
    """
    Subtract without login should return 401 Unauthorized.
    """
    response = client.get("/subtract/10/3")
    assert response.status_code == 401
    body = response.get_json()
    assert "unauthorized" in body["error"]


def test_subtract_after_login(client):
    """
    After a successful login, subtract should work.
    """
    # first login
    login_response = client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert login_response.status_code == 200

    # then call subtract
    response = client.get("/subtract/10/3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 7}
