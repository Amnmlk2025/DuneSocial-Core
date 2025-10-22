import json, pytest
from django.test import Client

@pytest.mark.django_db
def test_challenge_and_xp():
    c = Client()
    # create challenge
    r = c.post("/challenges", data=json.dumps({"title":"7-day reading","duration_days":7}), content_type="application/json")
    assert r.status_code == 201
    # create action
    r = c.post("/action-items", data=json.dumps({"title":"Read 10 pages"}), content_type="application/json")
    aid = r.json()["id"]
    # complete action -> one ProgressEvent => xp = 10
    r = c.post(f"/action-items/{aid}/complete"); assert r.status_code == 201
    r = c.get("/progress/xp"); assert r.status_code == 200 and r.json()["xp"] >= 10
