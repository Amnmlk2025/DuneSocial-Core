from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
from itertools import count

# --- in-memory stores for tests ---
_users = {}
_posts = {}
_challenges = {}
_actions = {}

_user_ids = count(1)
_post_ids = count(1)
_ch_ids = count(1)
_ai_ids = count(1)

def _json(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except Exception:
        return {}

def health(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return JsonResponse({"ok": True})

@csrf_exempt
def users(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = _json(request)
    username = (data.get("username") or "").strip()
    if not username:
        return JsonResponse({"error": "username required"}, status=400)
    uid = next(_user_ids)
    _users[uid] = {"id": uid, "username": username}
    return JsonResponse(_users[uid], status=201)

@csrf_exempt
def posts(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = _json(request)
    text = (data.get("text") or "").strip()
    author_id = data.get("author_id")
    if not text or not author_id:
        return JsonResponse({"error": "text and author_id required"}, status=400)
    if author_id not in _users:
        return JsonResponse({"error": "author not found"}, status=404)
    pid = next(_post_ids)
    _posts[pid] = {"id": pid, "text": text, "author_id": author_id, "likes": 0}
    return JsonResponse(_posts[pid], status=201)

@csrf_exempt
def post_like(request, post_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if post_id not in _posts:
        return JsonResponse({"error": "post not found"}, status=404)
    _posts[post_id]["likes"] += 1
    return JsonResponse({"id": post_id, "likes": _posts[post_id]["likes"]})

def feed(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    items = sorted(_posts.values(), key=lambda x: x["id"], reverse=True)[:50]
    return JsonResponse({"items": items})

@csrf_exempt
def challenges(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = _json(request)
    title = (data.get("title") or "").strip()
    duration_days = data.get("duration_days")
    if not title or duration_days is None:
        return JsonResponse({"error": "title and duration_days required"}, status=400)
    cid = next(_ch_ids)
    _challenges[cid] = {"id": cid, "title": title, "duration_days": duration_days}
    return JsonResponse(_challenges[cid], status=201)

@csrf_exempt
def action_items(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = _json(request)
    title = (data.get("title") or "").strip()
    if not title:
        return JsonResponse({"error": "title required"}, status=400)
    aid = next(_ai_ids)
    _actions[aid] = {"id": aid, "title": title}
    return JsonResponse(_actions[aid], status=201)
