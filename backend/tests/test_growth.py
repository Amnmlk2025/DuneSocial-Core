import json
import pytest
from django.test import Client

@pytest.mark.django_db
def test_action_flow():
    c = Client()
    r = c.post("/action-items", data=json.dumps({"title":"Read 10 pages"}), content_type="application/json")
    assert r.status_code == 201
    aid = r.json()["id"]
    r = c.get("/action-items")
    assert r.status_code == 200 and len(r.json()) >= 1
    r = c.post(f"/action-items/{aid}/complete")
    assert r.status_code == 201 and r.json()["type"] == "action_completed"
    r = c.get("/progress/timeline")
    assert r.status_code == 200 and any(ev["type"]=="action_completed" for ev in r.json())
