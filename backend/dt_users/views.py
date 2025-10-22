from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

@api_view(["GET","POST"])
def users(request):
    if request.method == "POST":
        s = UserSerializer(data=request.data); s.is_valid(raise_exception=True)
        u = s.save(); return Response(UserSerializer(u).data, status=201)
    return Response(UserSerializer(User.objects.order_by("-id"), many=True).data)
