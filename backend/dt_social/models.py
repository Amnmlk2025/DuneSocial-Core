from django.db import models
from django.utils import timezone
class Post(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    class Meta: app_label = "dt_social"
