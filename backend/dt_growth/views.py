from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ActionItem, ProgressEvent
from .serializers import ActionItemSerializer, ProgressEventSerializer

@api_view(["GET","POST"])
def action_items(request):
    if request.method == "POST":
        ser = ActionItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(ActionItemSerializer(obj).data, status=status.HTTP_201_CREATED)
    qs = ActionItem.objects.order_by("-id")
    return Response(ActionItemSerializer(qs, many=True).data)

@api_view(["POST"])
def action_complete(request, pk: int):
    try:
        ai = ActionItem.objects.get(pk=pk)
    except ActionItem.DoesNotExist:
        return Response({"detail":"not found"}, status=404)
    ai.is_done = True
    ai.save(update_fields=["is_done"])
    pe = ProgressEvent.objects.create(type="action_completed", action=ai, meta={"source":"api"})
    return Response(ProgressEventSerializer(pe).data, status=201)

@api_view(["GET"])
def progress_timeline(request):
    qs = ProgressEvent.objects.order_by("-at","-id")[:100]
    return Response(ProgressEventSerializer(qs, many=True).data)
