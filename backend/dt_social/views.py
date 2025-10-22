@csrf_exempt
def like_post(request, post_id):
    if request.method == "POST":
        try:
            p = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        p.likes += 1
        p.save(update_fields=["likes"])
        return JsonResponse({"id": p.id, "likes": p.likes}, status=200)
    return HttpResponseNotAllowed(["POST"])
