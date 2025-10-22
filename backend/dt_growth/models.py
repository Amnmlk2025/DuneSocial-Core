from django.db import models
from django.utils import timezone

class ActionItem(models.Model):
    title = models.CharField(max_length=200)
    due_at = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta: app_label = "dt_growth"

class ProgressEvent(models.Model):
    TYPE_CHOICES = (("action_completed","action_completed"),("note","note"))
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    action = models.ForeignKey(ActionItem, null=True, blank=True, on_delete=models.SET_NULL)
    at = models.DateTimeField(default=timezone.now)
    meta = models.JSONField(default=dict, blank=True)
    class Meta: app_label = "dt_growth"

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    duration_days = models.PositiveIntegerField(default=7)
    rules = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    class Meta: app_label = "dt_growth"
