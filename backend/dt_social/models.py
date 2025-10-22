from django.db import models
from django.utils import timezone

class Post(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    author_id = models.IntegerField(null=True, blank=True)  # Ê«»” êÌ ”»ò »Â dt_users.User »œÊ‰ FK Ê«ﬁ⁄Ì
    class Meta: app_label = "dt_social"
