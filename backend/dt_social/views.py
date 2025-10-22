import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Challenge, ActionItem

# ---------- Health ----------
@csrf_exempt
def health(request):
    return JsonResponse({"status": "ok"}, status=200)

# ---------- Users ----------
@csrf_exempt
def users(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        u = User.objects.create(username=data.get("username", ""))
        return JsonResponse({"id": u.id, "username": u.username}, status=201)
    if request.method == "GET":
        return JsonResponse(list(User.objects.values("id", "username")), safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])

# ---------- Posts ----------
@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        aid = data.get("author_id")
        try:
            author = User.objects.get(id=aid)
        except User.DoesNotExist:
            return JsonResponse({"error": "Author not found"}, status=404)
        p = Post.objects.create(text=data.get("text", ""), author=author)
        return JsonResponse(
            {"id": p.id, "text": p.text, "author_id": author.id, "likes": p.likes},
            status=201,
        )
    if request.method == "GET":
        return JsonResponse(list(Post.objects.values("id", "text", "author_id", "likes")), safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def like_post(request, post_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        p = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    p.likes += 1
    p.save(update_fields=["likes"])
    return JsonResponse({"id": p.id, "likes": p.likes}, status=200)

# ---------- Feed ----------
@csrf_exempt
def feed(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    uid = request.GET.get("user_id")
    qs = Post.objects.filter(author_id=uid).values("id", "text", "likes")
    return JsonResponse(list(qs), safe=False)

# ---------- Challenges ----------
@csrf_exempt
def challenges(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        c = Challenge.objects.create(
            title=data.get("title", ""),
            duration_days=data.get("duration_days", 0),
        )
        return JsonResponse(
            {"id": c.id, "title": c.title, "duration_days": c.duration_days},
            status=201,
        )
    if request.method == "GET":
        return JsonResponse(list(Challenge.objects.values("id", "title", "duration_days")), safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])

# ---------- Action Items ----------
@csrf_exempt
def action_items(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        a = ActionItem.objects.create(title=data.get("title", ""))
        return JsonResponse({"id": a.id, "title": a.title, "completed": a.completed}, status=201)
    if request.method == "GET":
        return JsonResponse(list(ActionItem.objects.values("id", "title", "completed")), safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def action_done(request, item_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        a = ActionItem.objects.get(id=item_id)
    except ActionItem.DoesNotExist:
        return JsonResponse({"error": "ActionItem not found"}, status=404)
    a.completed = True
    a.save(update_fields=["completed"])
    return JsonResponse({"id": a.id, "title": a.title, "completed": a.completed}, status=200)
