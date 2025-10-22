from rest_framework import serializers
from .models import ActionItem, ProgressEvent

class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = ["id","title","due_at","is_done","created_at"]

class ProgressEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressEvent
        fields = ["id","type","action","at","meta"]
