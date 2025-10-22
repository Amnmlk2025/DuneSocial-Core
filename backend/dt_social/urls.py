from django.urls import path
from . import views

urlpatterns = [
    path("health", views.health),
    path("users", views.users),
    path("posts", views.posts),
    path("posts/<int:post_id>/like", views.post_like),
    path("feed", views.feed),
    path("challenges", views.challenges),
    path("action-items", views.action_items),
]
