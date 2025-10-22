from django.urls import path
from . import views

urlpatterns = [
    # health
    path("health", views.health),

    # users
    path("users", views.users),

    # posts
    path("posts", views.posts),
    path("posts/<int:post_id>/like", views.post_like),

    # feed
    path("feed", views.feed),

    # growth
    path("challenges", views.challenges),
    path("action-items", views.action_items),
]
