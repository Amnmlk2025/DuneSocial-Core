from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta: app_label = "dt_users"
