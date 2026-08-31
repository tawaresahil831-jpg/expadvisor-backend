def test_notifications_workflow(client, auth_headers):
    # 1. Fetch initial notifications (creates welcome notification if none exist)
    res = client.get("/api/notifications", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert len(data) >= 1
    notif_id = data[0]["id"]
    assert data[0]["is_read"] is False

    # 2. Check unread count
    count_res = client.get("/api/notifications/unread-count", headers=auth_headers)
    assert count_res.status_code == 200
    assert count_res.get_json()["data"]["unread_count"] >= 1

    # 3. Mark single notification as read
    read_res = client.put(f"/api/notifications/{notif_id}/read", headers=auth_headers)
    assert read_res.status_code == 200

    # 4. Check unread count decremented
    count_res2 = client.get("/api/notifications/unread-count", headers=auth_headers)
    assert count_res2.status_code == 200
    assert count_res2.get_json()["data"]["unread_count"] == 0

    # 5. Mark all read
    all_read_res = client.put("/api/notifications/read-all", headers=auth_headers)
    assert all_read_res.status_code == 200

def test_bookmarks_workflow(client, auth_headers):
    # 1. Create an experience to bookmark
    exp_res = client.post("/api/experiences", headers=auth_headers, json={
        "title": "Experience to Bookmark",
        "content": "Valuable tips and strategies for passing technical interviews.",
        "category": "placement"
    })
    exp_id = exp_res.get_json()["data"]["experience_id"]

    # 2. Add bookmark (toggle ON)
    bm_res = client.post(f"/api/experiences/{exp_id}/bookmark", headers=auth_headers)
    assert bm_res.status_code == 201
    assert bm_res.get_json()["data"]["is_bookmarked"] is True

    # 3. Fetch user bookmarks
    get_bm_res = client.get("/api/bookmarks", headers=auth_headers)
    assert get_bm_res.status_code == 200
    data = get_bm_res.get_json()["data"]
    assert len(data) == 1
    assert data[0]["experience_id"] == exp_id

    # 4. Remove bookmark (toggle OFF)
    un_bm_res = client.post(f"/api/experiences/{exp_id}/bookmark", headers=auth_headers)
    assert un_bm_res.status_code == 200
    assert un_bm_res.get_json()["data"]["is_bookmarked"] is False

    # 5. Verify bookmarks list empty
    get_bm_res2 = client.get("/api/bookmarks", headers=auth_headers)
    assert len(get_bm_res2.get_json()["data"]) == 0

