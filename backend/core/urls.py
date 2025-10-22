from django.urls import path, include
from .views import health

urlpatterns = [
    path("health", health),
    path("", include("dt_growth.urls")),
    path("", include("dt_social.urls")),
    path("", include("dt_users.urls")),
]