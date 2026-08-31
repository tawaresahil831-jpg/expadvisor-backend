import requests
import uuid
import sys

BASE_URL = "http://127.0.0.1:5001/api"
session = requests.Session()

def run_tests():
    # 1. Register
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "password123"
    
    print("--- 1. Registering user ---")
    res = session.post(f"{BASE_URL}/auth/register", json={
        "name": "Test User",
        "email": test_email,
        "password": test_password,
        "college": "MIT College",
        "branch": "Computer Engineering",
        "year": 3,
        "skills": "Python, Flask, JavaScript"
    })
    print(res.status_code, res.json())
    assert res.status_code == 201

    reg_data = res.json().get("data", {})
    if res.json().get("requires_verification"):
        dev_otp = reg_data.get("dev_otp")
        print(f"\n--- 1.1 Verifying Email with OTP {dev_otp} ---")
        res_v = session.post(f"{BASE_URL}/auth/verify-otp", json={
            "email": test_email,
            "otp": dev_otp
        })
        print(res_v.status_code, res_v.json())
        assert res_v.status_code == 200

    # 2. Login
    print("\n--- 2. Logging in ---")
    res = session.post(f"{BASE_URL}/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    print(res.status_code, res.json())
    assert res.status_code == 200
    token = res.json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    session.headers.update(headers)

    # 3. Create Experience
    print("\n--- 3. Creating Experience ---")
    res = session.post(f"{BASE_URL}/experiences", json={
        "title": "Test Experience",
        "content": "This is a test experience content"
    })
    print(res.status_code, res.json())
    assert res.status_code == 201
    exp_id = res.json()["data"]["experience_id"]

    # 4. Get Experience (Single)
    print("\n--- 4. Getting Experience (Single) ---")
    res = session.get(f"{BASE_URL}/experiences/{exp_id}")
    print(res.status_code, res.json())
    assert res.status_code == 200

    # 4.1 List Experiences (Pagination & Filter)
    print("\n--- 4.1. List Experiences (Pagination & Filter) ---")
    res = session.get(f"{BASE_URL}/experiences?page=1&per_page=5&search=Test")
    print(res.status_code, res.json())
    assert res.status_code == 200
    assert "pagination" in res.json()
    assert res.json()["pagination"]["total_items"] >= 1

    # 5. Update Experience (Ownership check implicitly passes as we are the creator)
    print("\n--- 5. Updating Experience ---")
    res = session.put(f"{BASE_URL}/experiences/{exp_id}", json={
        "title": "Updated Test Experience"
    })
    print(res.status_code, res.json())
    assert res.status_code == 200

    # 5.1 Upload File
    print("\n--- 5.1 Uploading File ---")
    files = {'file': ('dummy.pdf', b'dummy content for pdf', 'application/pdf')}
    res = session.post(f"{BASE_URL}/experiences/{exp_id}/upload", files=files)
    print(res.status_code, res.json())
    assert res.status_code == 200
    assert "file_url" in res.json()["data"]
    assert res.json()["data"]["file_url"] is not None

    # 6. Comments
    print("\n--- 6. Testing Comments (POST) ---")
    res = session.post(f"{BASE_URL}/experiences/{exp_id}/comments", json={
        "comment": "This is a test comment"
    })
    print(res.status_code, res.json())
    assert res.status_code == 201
    comment_id = res.json()["data"]["comment_id"]

    print("\n--- Testing Comments (GET) ---")
    res = session.get(f"{BASE_URL}/experiences/{exp_id}/comments")
    print(res.status_code, res.json())
    assert res.status_code == 200
    assert len(res.json()["data"]) > 0

    print("\n--- Testing Comments (DELETE) ---")
    res = session.delete(f"{BASE_URL}/comments/{comment_id}")
    print(res.status_code, res.json())
    assert res.status_code == 200

    # 7. Test Likes
    print("\n--- 7. Testing Likes (POST) ---")
    res = session.post(f"{BASE_URL}/experiences/{exp_id}/like")
    print(res.status_code, res.json())
    assert res.status_code == 201

    print("\n--- Testing Likes (GET) ---")
    res = session.get(f"{BASE_URL}/experiences/{exp_id}/likes")
    print(res.status_code, res.json())
    assert res.status_code == 200
    assert res.json()["data"]["like_count"] == 1

    print("\n--- Testing Likes (DELETE) ---")
    res = session.delete(f"{BASE_URL}/experiences/{exp_id}/like")
    print(res.status_code, res.json())
    assert res.status_code == 200

    # 8. Delete Experience
    print("\n--- 8. Deleting Experience ---")
    res = session.delete(f"{BASE_URL}/experiences/{exp_id}")
    print(res.status_code, res.json())
    assert res.status_code == 200
    
    print("\nALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
