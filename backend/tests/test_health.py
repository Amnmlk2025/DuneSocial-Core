def test_health(client):
    from django.test import Client
    c = Client()
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
