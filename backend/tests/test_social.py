import json, pytest
from django.test import Client

@pytest.mark.django_db
def test_posts_flow():
    c = Client()
    r = c.post("/posts", data=json.dumps({"text":"hello dune"}), content_type="application/json")
    assert r.status_code == 201
    pid = r.json()["id"]
    r = c.get("/posts"); assert r.status_code == 200 and any(p["id"]==pid for p in r.json())
    r = c.post(f"/posts/{pid}/like"); assert r.status_code == 200 and r.json()["likes"] == 1
