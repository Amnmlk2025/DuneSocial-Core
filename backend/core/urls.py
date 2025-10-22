from django.contrib import admin
from django.urls import path, include

# تلاش برای اطمینان از وجود /health حتی اگر dt_social/urls کامل نباشد
try:
    import dt_social.views as v  # type: ignore
    extra_patterns = [path("health", v.health)]
except Exception:
    extra_patterns = []

urlpatterns = [
    path("admin/", admin.site.urls),
    *extra_patterns,
    path("", include("dt_social.urls")),
]
