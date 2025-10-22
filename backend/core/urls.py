from django.urls import path, include

urlpatterns = [
    # بدون پیشوند تا /users ، /posts ، /feed و /health کار کنند
    path("", include("dt_social.urls")),
]
