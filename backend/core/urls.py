from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # بدون پیشوند؛ تا /users ، /posts ، /feed کار کنند
    path("", include("dt_social.urls")),
]
