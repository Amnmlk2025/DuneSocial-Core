from django.urls import path
from .views import posts, like, feed
urlpatterns = [
    path("posts", posts),
    path("posts/<int:pk>/like", like),
    path("feed", feed),
]
