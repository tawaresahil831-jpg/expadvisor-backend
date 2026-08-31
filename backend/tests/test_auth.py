import json

def test_register_success(client):
    res = client.post("/api/auth/register", json={
        "name": "Bob Builder",
        "email": "bob@example.com",
        "password": "password123",
        "college": "MIT",
        "branch": "Mechanical",
        "year": 2,
        "skills": "CAD, Robotics"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["requires_verification"] is True
    assert "dev_otp" in data["data"]

def test_register_validation_failure(client):
    res = client.post("/api/auth/register", json={
        "name": "X",
        "email": "invalid-email"
    })
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "errors" in data

def test_register_duplicate_email(client, test_user):
    res = client.post("/api/auth/register", json={
        "name": "Another User",
        "email": test_user["email"],
        "password": "password123",
        "college": "MIT",
        "branch": "CS",
        "year": 1,
        "skills": "Python"
    })
    assert res.status_code == 409
    data = res.get_json()
    assert data["success"] is False

def test_verify_otp_and_login(client):
    # Register
    reg_res = client.post("/api/auth/register", json={
        "name": "Charlie Tester",
        "email": "charlie@example.com",
        "password": "password123",
        "college": "UC Berkeley",
        "branch": "EECS",
        "year": 3,
        "skills": "Go, Docker"
    })
    otp = reg_res.get_json()["data"]["dev_otp"]
    
    # Verify OTP
    verify_res = client.post("/api/auth/verify-otp", json={
        "email": "charlie@example.com",
        "otp": otp
    })
    assert verify_res.status_code == 200
    assert verify_res.get_json()["success"] is True

    # Login
    login_res = client.post("/api/auth/login", json={
        "email": "charlie@example.com",
        "password": "password123"
    })
    assert login_res.status_code == 200
    assert "token" in login_res.get_json()["data"]

def test_get_me(client, auth_headers, test_user):
    res = client.get("/api/auth/me", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["email"] == test_user["email"]
