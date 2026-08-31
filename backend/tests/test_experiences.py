def test_create_experience(client, auth_headers):
    res = client.post("/api/experiences", headers=auth_headers, json={
        "title": "Software Engineering Internship",
        "content": "Worked on distributed systems and microservices architecture at scale.",
        "category": "internship",
        "semester": "6th",
        "company": "Google"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["title"] == "Software Engineering Internship"
    assert data["data"]["company"] == "Google"

def test_get_experiences_pagination_and_filter(client, auth_headers):
    # Create 2 experiences
    client.post("/api/experiences", headers=auth_headers, json={
        "title": "Internship Experience at Meta",
        "content": "Great mentorship program and high impact engineering projects.",
        "category": "internship",
        "company": "Meta"
    })
    client.post("/api/experiences", headers=auth_headers, json={
        "title": "Placement at Microsoft",
        "content": "Comprehensive interview process focusing on data structures and algorithms.",
        "category": "placement",
        "company": "Microsoft"
    })

    # Fetch with filter
    res = client.get("/api/experiences?category=internship")
    assert res.status_code == 200
    data = res.get_json()
    assert data["pagination"]["total_items"] >= 1
    assert all(item["category"] == "internship" for item in data["data"])

def test_get_single_experience_and_view_count(client, auth_headers):
    create_res = client.post("/api/experiences", headers=auth_headers, json={
        "title": "Single Experience Test Post",
        "content": "Detailed overview of interview rounds and practical advice for juniors.",
        "category": "placement"
    })
    exp_id = create_res.get_json()["data"]["experience_id"]

    res = client.get(f"/api/experiences/{exp_id}")
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["experience_id"] == exp_id
    assert data["views"] >= 1

def test_update_and_delete_experience_ownership(client, auth_headers):
    # Create experience
    create_res = client.post("/api/experiences", headers=auth_headers, json={
        "title": "Original Experience Title",
        "content": "Original experience content description with detailed advice.",
        "category": "project"
    })
    exp_id = create_res.get_json()["data"]["experience_id"]

    # Update with owner auth
    update_res = client.put(f"/api/experiences/{exp_id}", headers=auth_headers, json={
        "title": "Updated Experience Title"
    })
    assert update_res.status_code == 200
    assert update_res.get_json()["data"]["title"] == "Updated Experience Title"

    # Delete without auth should fail
    unauth_delete = client.delete(f"/api/experiences/{exp_id}")
    assert unauth_delete.status_code == 401

    # Delete with owner auth
    delete_res = client.delete(f"/api/experiences/{exp_id}", headers=auth_headers)
    assert delete_res.status_code == 200

    # Getting after delete should be 404
    get_res = client.get(f"/api/experiences/{exp_id}")
    assert get_res.status_code == 404
