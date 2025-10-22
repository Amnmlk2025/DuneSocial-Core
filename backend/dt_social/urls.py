from django.urls import path
from .views import posts, like
urlpatterns = [
    path("posts", posts),
    path("posts/<int:pk>/like", like),
]
