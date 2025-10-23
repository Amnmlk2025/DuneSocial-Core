import json
from uuid import uuid4
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Challenge, ActionItem

def health(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def users(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        u = User.objects.create(username=data.get("username", ""))
        return JsonResponse({"id": u.id, "username": u.username}, status=201)
    if request.method == "GET":
        return JsonResponse(
            [{"id": u.id, "username": u.username} for u in User.objects.all()],
            safe=False,
        )
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        # author_id اختیاری است؛ اگر نبود یک کاربر ناشناس می‌سازیم تا تست‌ها ۲۰۱ بگیرند
        author_id = data.get("author_id")
        author = None
        if author_id:
            author = User.objects.filter(id=author_id).first()
            if not author:
                return JsonResponse({"error": "author not found"}, status=404)
        else:
            author = User.objects.create(username=f"anon_{uuid4().hex[:8]}")

        p = Post.objects.create(text=data.get("text", ""), author=author)
        return JsonResponse(
            {"id": p.id, "text": p.text, "author_id": p.author_id, "likes": p.likes},
            status=201,
        )
    if request.method == "GET":
        return JsonResponse(
            [
                {"id": p.id, "text": p.text, "author_id": p.author_id, "likes": p.likes}
                for p in Post.objects.order_by("-id")
            ],
            safe=False,
        )
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def like_post(request, pid: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    p = Post.objects.filter(id=pid).first()
    if not p:
        return JsonResponse({"error": "not found"}, status=404)
    p.likes += 1
    p.save(update_fields=["likes"])
    return JsonResponse({"id": p.id, "likes": p.likes})

def feed(request):
    uid = request.GET.get("user_id")
    qs = Post.objects.all()
    if uid:
        qs = qs.filter(author_id=uid)
    return JsonResponse(
        [
            {"id": p.id, "text": p.text, "author_id": p.author_id, "likes": p.likes}
            for p in qs.order_by("-id")
        ],
        safe=False,
    )

@csrf_exempt
def challenges(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        c = Challenge.objects.create(
            title=data.get("title", ""), duration_days=int(data.get("duration_days", 0))
        )
        return JsonResponse(
            {"id": c.id, "title": c.title, "duration_days": c.duration_days}, status=201
        )
    if request.method == "GET":
        return JsonResponse(
            [
                {"id": c.id, "title": c.title, "duration_days": c.duration_days}
                for c in Challenge.objects.order_by("-id")
            ],
            safe=False,
        )
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def action_items(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        a = ActionItem.objects.create(title=data.get("title", ""), completed=False)
        return JsonResponse(
            {"id": a.id, "title": a.title, "completed": a.completed}, status=201
        )
    if request.method == "GET":
        return JsonResponse(
            [
                {"id": a.id, "title": a.title, "completed": a.completed}
                for a in ActionItem.objects.order_by("-id")
            ],
            safe=False,
        )
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def action_done(request, aid: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    a = ActionItem.objects.filter(id=aid).first()
    if not a:
        return JsonResponse({"error": "not found"}, status=404)
    a.completed = True
    a.save(update_fields=["completed"])
    return JsonResponse({"id": a.id, "title": a.title, "completed": a.completed})
