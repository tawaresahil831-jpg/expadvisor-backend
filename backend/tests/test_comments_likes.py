def test_comments_flow(client, auth_headers):
    # Create experience
    exp_res = client.post("/api/experiences", headers=auth_headers, json={
        "title": "Experience for Comment Discussion",
        "content": "Discussing specific technical questions asked during the technical round.",
        "category": "internship"
    })
    exp_id = exp_res.get_json()["data"]["experience_id"]

    # Post comment
    comment_res = client.post(f"/api/experiences/{exp_id}/comments", headers=auth_headers, json={
        "comment": "Did they ask about dynamic programming?"
    })
    assert comment_res.status_code == 201
    comment_data = comment_res.get_json()["data"]
    comment_id = comment_data["comment_id"]

    # Get comments
    get_res = client.get(f"/api/experiences/{exp_id}/comments")
    assert get_res.status_code == 200
    assert len(get_res.get_json()["data"]) >= 1

    # Mark as accepted answer (if endpoint exists)
    accept_res = client.post(f"/api/experiences/{exp_id}/comments/{comment_id}/accept", headers=auth_headers)
    if accept_res.status_code != 404:
        assert accept_res.status_code == 200

    # Delete comment
    del_res = client.delete(f"/api/comments/{comment_id}", headers=auth_headers)
    assert del_res.status_code == 200

def test_likes_toggle(client, auth_headers):
    # Create experience
    exp_res = client.post("/api/experiences", headers=auth_headers, json={
        "title": "Experience for Like Testing",
        "content": "Valuable advice on resume building and behavioral interview preparation.",
        "category": "placement"
    })
    exp_id = exp_res.get_json()["data"]["experience_id"]

    # Add like
    like_res = client.post(f"/api/experiences/{exp_id}/like", headers=auth_headers)
    assert like_res.status_code == 201
    assert like_res.get_json()["data"]["like_count"] == 1

    # Check like count
    count_res = client.get(f"/api/experiences/{exp_id}/likes")
    assert count_res.status_code == 200
    assert count_res.get_json()["data"]["like_count"] == 1

    # Remove like
    unlike_res = client.delete(f"/api/experiences/{exp_id}/like", headers=auth_headers)
    assert unlike_res.status_code == 200
    assert unlike_res.get_json()["data"]["like_count"] == 0
