from django.urls import path
from . import views

urlpatterns = [
    # health
    path("health", views.health),
    path("health/", views.health),

    # users
    path("users", views.users),
    path("users/", views.users),

    # posts
    path("posts", views.posts),
    path("posts/", views.posts),
    path("posts/<int:post_id>/like", views.post_like),
    path("posts/<int:post_id>/like/", views.post_like),

    # feed
    path("feed", views.feed),
    path("feed/", views.feed),

    # challenges
    path("challenges", views.challenges),
    path("challenges/", views.challenges),

    # action-items
    path("action-items", views.action_items),
    path("action-items/", views.action_items),
]
