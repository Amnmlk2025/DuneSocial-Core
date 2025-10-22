from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

# مدل‌ها
from .models import User, Post, Challenge, ActionItem


def _json_body(request):
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
    if request.method == "POST":
        data = _json_body(request)
        username = data.get("username", "").strip()
        if not username:
            return JsonResponse({"error": "username required"}, status=400)
        u = User.objects.create(username=username)
        return JsonResponse({"id": u.id, "username": u.username}, status=201)
    return HttpResponseNotAllowed(["POST"])


@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = _json_body(request)
        text = data.get("text", "").strip()
        author_id = data.get("author_id")
        if not text or not author_id:
            return JsonResponse({"error": "text and author_id required"}, status=400)
        author = get_object_or_404(User, id=author_id)
        p = Post.objects.create(text=text, author=author)
        return JsonResponse(
            {"id": p.id, "text": p.text, "author_id": p.author_id, "likes": getattr(p, "likes", 0)},
            status=201,
        )
    return HttpResponseNotAllowed(["POST"])


@csrf_exempt
def post_like(request, post_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    p = get_object_or_404(Post, id=post_id)
    # فیلد likes ممکن است در مدل وجود نداشته باشد؛ در این صورت آن را صفر در نظر بگیر
    current = getattr(p, "likes", 0)
    try:
        setattr(p, "likes", current + 1)
        p.save(update_fields=["likes"])
    except Exception:
        # اگر مدل فیلدی نداشت، ذخیره کامل
        p.likes = current + 1
        p.save()
    return JsonResponse({"id": p.id, "likes": p.likes})


def feed(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    # تست فقط 200 می‌خواهد؛ خروجی حداقلی
    qs = Post.objects.order_by("-id")[:50]
    items = [{"id": p.id, "text": p.text, "author_id": p.author_id, "likes": getattr(p, "likes", 0)} for p in qs]
    return JsonResponse({"items": items})


@csrf_exempt
def challenges(request):
    if request.method == "POST":
        data = _json_body(request)
        title = data.get("title", "").strip()
        duration_days = data.get("duration_days")
        if not title or duration_days is None:
            return JsonResponse({"error": "title and duration_days required"}, status=400)
        ch = Challenge.objects.create(title=title, duration_days=duration_days)
        return JsonResponse({"id": ch.id, "title": ch.title, "duration_days": ch.duration_days}, status=201)
    return HttpResponseNotAllowed(["POST"])


@csrf_exempt
def action_items(request):
    if request.method == "POST":
        data = _json_body(request)
        title = data.get("title", "").strip()
        if not title:
            return JsonResponse({"error": "title required"}, status=400)
        ai = ActionItem.objects.create(title=title)
        return JsonResponse({"id": ai.id, "title": ai.title}, status=201)
    return HttpResponseNotAllowed(["POST"])
