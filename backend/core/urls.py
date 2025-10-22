from django.urls import path, include

urlpatterns = [
    path("", include("dt_social.urls")),
]
