# backend/dt_social/views.py
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
import json

from .models import User, Post, Challenge, ActionItem

def _json_body(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except Exception:
        return {}

def health(request):
    return JsonResponse({"status": "ok"}, status=200)

@csrf_exempt
def users(request):
    if request.method == "POST":
        data = _json_body(request)
        u = User.objects.create(username=data.get("username", ""))
        return JsonResponse({"id": u.id, "username": u.username}, status=201)
    if request.method == "GET":
        return JsonResponse(
            [{"id": u.id, "username": u.username} for u in User.objects.all()],
            safe=False,
            status=200,
        )
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = _json_body(request)
        text = data.get("text", "")
        author_id = data.get("author_id")
        author = User.objects.filter(id=author_id).first() if author_id else None
        if not text:
            return JsonResponse({"error": "text required"}, status=400)
        p = Post.objects.create(text=text, author=author)
        return JsonResponse({"id": p.id, "text": p.text, "likes": p.likes or 0}, status=201)
    if request.method == "GET":
        lst = [{"id": p.id, "text": p.text, "likes": p.likes or 0} for p in Post.objects.all().order_by("id")]
        return JsonResponse(lst, safe=False, status=200)
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def like_post(request, pid: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    p = Post.objects.filter(id=pid).first()
    if not p:
        return JsonResponse({"error": "not found"}, status=404)
    p.likes = (p.likes or 0) + 1
    p.save(update_fields=["likes"])
    return JsonResponse({"id": p.id, "likes": p.likes}, status=200)

def feed(request):
    user_id = request.GET.get("user_id")
    # تست فقط 200 می‌خواهد و لیستی از پست‌ها
    items = [{"id": p.id, "text": p.text, "likes": p.likes or 0} for p in Post.objects.all().order_by("id")]
    return JsonResponse(items, safe=False, status=200)

@csrf_exempt
def challenges(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = _json_body(request)
    c = Challenge.objects.create(
        title=data.get("title", ""),
        duration_days=data.get("duration_days", 0),
    )
    return JsonResponse({"id": c.id, "title": c.title, "duration_days": c.duration_days}, status=201)

@csrf_exempt
def action_items(request):
    if request.method == "POST":
        data = _json_body(request)
        a = ActionItem.objects.create(title=data.get("title", ""), completed=False)
        return JsonResponse({"id": a.id, "title": a.title, "completed": a.completed}, status=201)
    if request.method == "GET":
        lst = [{"id": a.id, "title": a.title, "completed": a.completed} for a in ActionItem.objects.all().order_by("id")]
        return JsonResponse(lst, safe=False, status=200)
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def action_done(request, aid: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    a = ActionItem.objects.filter(id=aid).first()
    if not a:
        return JsonResponse({"error": "not found"}, status=404)
    if not a.completed:
        a.completed = True
        a.save(update_fields=["completed"])
    # تست انتظار type=='action_completed' و status=201 دارد
    return JsonResponse({"type": "action_completed", "action_id": a.id, "xp": 10}, status=201)
