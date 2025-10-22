from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}"


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    duration_days = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ActionItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({'done' if self.completed else 'todo'})"
