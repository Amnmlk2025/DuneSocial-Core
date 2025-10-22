import json, pytest
from django.test import Client

@pytest.mark.django_db
def test_user_and_feed_flow():
    c = Client()
    # user
    r = c.post("/users", data=json.dumps({"username":"amin"}), content_type="application/json")
    assert r.status_code == 201
    uid = r.json()["id"]
    # posts
    p1 = c.post("/posts", data=json.dumps({"text":"p1","author_id":uid}), content_type="application/json").json()
    p2 = c.post("/posts", data=json.dumps({"text":"p2","author_id":uid}), content_type="application/json").json()
    # like second
    r = c.post(f"/posts/{p2['id']}/like"); assert r.status_code == 200 and r.json()["likes"] == 1
    # personal feed
    r = c.get(f"/feed?user_id={uid}")
    assert r.status_code == 200
    ids = [x["id"] for x in r.json()]
    assert p1["id"] in ids and p2["id"] in ids
