import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Challenge, ActionItem

@csrf_exempt
def health(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def users(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = json.loads(request.body or "{}")
    u = User.objects.create(username=data.get("username", "user"))
    return JsonResponse({"id": u.id, "username": u.username}, status=201)

@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = json.loads(request.body or "{}")
        text = data.get("text", "")
        author = None
        author_id = data.get("author_id")
        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                author = None
        if author is None:
            author, _ = User.objects.get_or_create(username="anon")
        p = Post.objects.create(text=text, author=author)
        return JsonResponse({"id": p.id, "text": p.text, "likes": p.likes}, status=201)
    if request.method == "GET":
        out = [{"id": p.id, "text": p.text, "likes": p.likes} for p in Post.objects.order_by("id")]
        return JsonResponse(out, safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def like_post(request, post_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        p = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    p.likes = (p.likes or 0) + 1
    p.save(update_fields=["likes"])
    return JsonResponse({"id": p.id, "likes": p.likes})

def feed(request):
    user_id = request.GET.get("user_id")
    try:
        u = User.objects.get(id=user_id)
    except Exception:
        return HttpResponseNotFound()
    posts = Post.objects.filter(author=u).order_by("id")
    out = [{"id": p.id, "text": p.text, "likes": p.likes} for p in posts]
    return JsonResponse(out, safe=False)

@csrf_exempt
def challenges(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = json.loads(request.body or "{}")
    ch = Challenge.objects.create(
        title=data.get("title", ""),
        duration_days=data.get("duration_days", 0),
    )
    return JsonResponse({"id": ch.id, "title": ch.title, "duration_days": ch.duration_days}, status=201)

@csrf_exempt
def action_items(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    data = json.loads(request.body or "{}")
    a = ActionItem.objects.create(title=data.get("title", ""))
    return JsonResponse({"id": a.id, "title": a.title}, status=201)
