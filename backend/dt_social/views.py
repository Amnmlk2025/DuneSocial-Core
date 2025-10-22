from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

@api_view(["GET","POST"])
def posts(request):
    if request.method == "POST":
        s = PostSerializer(data=request.data); s.is_valid(raise_exception=True)
        obj = s.save(); return Response(PostSerializer(obj).data, status=201)
    qs = Post.objects.order_by("-id")[:100]
    return Response(PostSerializer(qs, many=True).data)

@api_view(["POST"])
def like(request, pk:int):
    try: p = Post.objects.get(pk=pk)
    except Post.DoesNotExist: return Response({"detail":"not found"}, status=404)
    p.likes += 1; p.save(update_fields=["likes"])
    return Response({"id": p.id, "likes": p.likes}, status=200)

@api_view(["GET"])
def feed(request):
    # ›Ìœ ⁄„Ê„Ì »« «„ò«‰ ›Ì· — ò«—»—: /feed?user_id=123
    uid = request.GET.get("user_id")
    qs = Post.objects.all()
    if uid:
        qs = qs.filter(author_id=int(uid))
    qs = qs.order_by("-id")[:100]
    return Response(PostSerializer(qs, many=True).data)
