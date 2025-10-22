import json
from django.test import Client

def test_action_flow():
    c = Client()
    # create
    r = c.post("/action-items", data=json.dumps({"title":"Read 10 pages"}), content_type="application/json")
    assert r.status_code == 201
    aid = r.json()["id"]
    # list
    r = c.get("/action-items")
    assert r.status_code == 200 and len(r.json()) >= 1
    # complete -> progress event
    r = c.post(f"/action-items/{aid}/complete")
    assert r.status_code == 201 and r.json()["type"] == "action_completed"
    # timeline
    r = c.get("/progress/timeline")
    assert r.status_code == 200 and any(ev["type"]=="action_completed" for ev in r.json())
