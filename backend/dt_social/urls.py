from django.urls import path
from . import views

urlpatterns = [
    path("health", views.health),

    path("users", views.users),

    path("posts", views.posts),
    path("posts/<int:pid>/like", views.like_post),

    path("feed", views.feed),

    path("challenges", views.challenges),

    path("action-items", views.action_items),
    path("action-items/<int:aid>/complete", views.action_done),
]
