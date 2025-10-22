from django.urls import path
from .views import action_items, action_complete, progress_timeline

urlpatterns = [
    path("action-items", action_items),
    path("action-items/<int:pk>/complete", action_complete),
    path("progress/timeline", progress_timeline),
]
