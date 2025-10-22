import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Challenge, ActionItem


def health(request):
    return JsonResponse({"status": "ok"})


def _parse_json(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except Exception:
        return {}


@csrf_exempt
def users(request):
    if request.method == "POST":
        data = _parse_json(request)
        u = User.objects.create(username=(data.get("username") or "").strip() or "anon")
        return JsonResponse({"id": u.id, "username": u.username}, status=201)
    if request.method == "GET":
        out = [{"id": u.id, "username": u.username} for u in User.objects.all().order_by("id")]
        return JsonResponse(out, safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])


def _post_to_dict(p: Post):
    return {"id": p.id, "text": p.text, "likes": p.likes, "author_id": p.author_id}


@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = _parse_json(request)
        p = Post.objects.create(
            text=(data.get("text") or "").strip(),
            author_id=data.get("author_id"),
        )
        return JsonResponse(_post_to_dict(p), status=201)
    if request.method == "GET":
        items = [_post_to_dict(p) for p in Post.objects.all().order_by("id")]
        return JsonResponse(items, safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def post_like(request, post_id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        p = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    p.likes = (p.likes or 0) + 1
    p.save(update_fields=["likes"])
    return JsonResponse({"likes": p.likes})


@csrf_exempt
def feed(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    user_id = request.GET.get("user_id")
    qs = Post.objects.all()
    if user_id:
        qs = qs.filter(author_id=user_id)
    items = [_post_to_dict(p) for p in qs.order_by("-id")]
    return JsonResponse(items, safe=False)


@csrf_exempt
def challenges(request):
    if request.method == "POST":
        data = _parse_json(request)
        ch = Challenge.objects.create(
            title=(data.get("title") or "").strip(),
            duration_days=int(data.get("duration_days") or 0),
        )
        return JsonResponse({"id": ch.id, "title": ch.title, "duration_days": ch.duration_days}, status=201)
    if request.method == "GET":
        items = [{"id": ch.id, "title": ch.title, "duration_days": ch.duration_days}
                 for ch in Challenge.objects.all().order_by("id")]
        return JsonResponse(items, safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def action_items(request):
    if request.method == "POST":
        data = _parse_json(request)
        ai = ActionItem.objects.create(title=(data.get("title") or "").strip(), done=False)
        return JsonResponse({"id": ai.id, "title": ai.title, "done": ai.done}, status=201)
    if request.method == "GET":
        items = [{"id": ai.id, "title": ai.title, "done": ai.done}
                 for ai in ActionItem.objects.all().order_by("id")]
        return JsonResponse(items, safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])
