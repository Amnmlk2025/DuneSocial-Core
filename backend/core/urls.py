from django.urls import path, include
urlpatterns = [
    path("", include("dt_growth.urls")),
]
