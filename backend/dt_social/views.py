import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Challenge, ActionItem

def _json(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except Exception:
        return {}

def health(_):
    return JsonResponse({"status": "ok"}, status=200)

@csrf_exempt
def users(request):
    if request.method == "POST":
        data = _json(request)
        u = User.objects.create(username=data.get("username", "").strip() or "user")
        return JsonResponse({"id": u.id, "username": u.username}, status=201)
    if request.method == "GET":
        out = [{"id": u.id, "username": u.username} for u in User.objects.all().order_by("id")]
        return JsonResponse(out, safe=False, status=200)
    return HttpResponseNotAllowed(["GET","POST"])

@csrf_exempt
def posts(request, post_id=None, action=None):
    if request.method == "POST" and post_id is None:
        data = _json(request)
        author = None
        aid = data.get("author_id")
        if aid:
            try:
                author = User.objects.get(id=aid)
            except User.DoesNotExist:
                pass
        p = Post.objects.create(text=data.get("text",""), author=author)
        return JsonResponse({"id": p.id, "text": p.text, "likes": p.likes, "author_id": p.author_id}, status=201)

    if request.method == "GET" and post_id is None:
        out = [{"id": p.id, "text": p.text, "likes": p.likes, "author_id": p.author_id}
               for p in Post.objects.all().order_by("id")]
        return JsonResponse(out, safe=False, status=200)

    if request.method == "POST" and post_id is not None and action == "like":
        p = Post.objects.get(id=post_id)
        p.likes += 1
        p.save(update_fields=["likes"])
        return JsonResponse({"id": p.id, "likes": p.likes}, status=200)

    return HttpResponseNotAllowed(["GET","POST"])

def feed(request):
    uid = request.GET.get("user_id")
    qs = Post.objects.all().order_by("-id")
    if uid:
        # نسخه ساده: فعلاً همان همه پست‌ها
        pass
    out = [{"id": p.id, "text": p.text, "likes": p.likes, "author_id": p.author_id} for p in qs]
    return JsonResponse(out, safe=False, status=200)

@csrf_exempt
def challenges(request):
    if request.method == "POST":
        data = _json(request)
        c = Challenge.objects.create(
            title=data.get("title",""),
            duration_days=int(data.get("duration_days", 0) or 0)
        )
        return JsonResponse({"id": c.id, "title": c.title, "duration_days": c.duration_days}, status=201)
    if request.method == "GET":
        out = [{"id": c.id, "title": c.title, "duration_days": c.duration_days}
               for c in Challenge.objects.all().order_by("id")]
        return JsonResponse(out, safe=False, status=200)
    return HttpResponseNotAllowed(["GET","POST"])

@csrf_exempt
def action_items(request, item_id=None, action=None):
    if request.method == "POST" and item_id is None:
        data = _json(request)
        a = ActionItem.objects.create(title=data.get("title",""))
        return JsonResponse({"id": a.id, "title": a.title, "completed": a.completed}, status=201)

    if request.method == "GET" and item_id is None:
        out = [{"id": a.id, "title": a.title, "completed": a.completed}
               for a in ActionItem.objects.all().order_by("id")]
        return JsonResponse(out, safe=False, status=200)

    if request.method == "POST" and item_id is not None and action == "complete":
        a = ActionItem.objects.get(id=item_id)
        a.completed = True
        a.save(update_fields=["completed"])
        return JsonResponse({"id": a.id, "title": a.title, "completed": a.completed}, status=200)

    return HttpResponseNotAllowed(["GET","POST"])
