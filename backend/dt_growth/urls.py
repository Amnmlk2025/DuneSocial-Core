from django.urls import path
from .views import action_items, action_complete, progress_timeline, progress_xp, challenges

urlpatterns = [
    path("action-items", action_items),
    path("action-items/<int:pk>/complete", action_complete),
    path("progress/timeline", progress_timeline),
    path("progress/xp", progress_xp),
    path("challenges", challenges),
]
