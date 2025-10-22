from django.urls import path
from . import views as v

urlpatterns = [
    path("health", v.health),

    path("users", v.users),

    path("posts", v.posts),
    path("posts/<int:post_id>/like", v.like_post),

    path("feed", v.feed),

    path("challenges", v.challenges),

    path("action-items", v.action_items),                         # GET لیست، POST ایجاد
    path("action-items/<int:item_id>/complete", v.action_done),   # POST تکمیل
]
