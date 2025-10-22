from rest_framework import serializers
from .models import ActionItem, ProgressEvent, Challenge

class ActionItemSerializer(serializers.ModelSerializer):
    class Meta: model = ActionItem; fields = ["id","title","due_at","is_done","created_at"]

class ProgressEventSerializer(serializers.ModelSerializer):
    class Meta: model = ProgressEvent; fields = ["id","type","action","at","meta"]

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta: model = Challenge; fields = ["id","title","duration_days","rules","created_at"]
