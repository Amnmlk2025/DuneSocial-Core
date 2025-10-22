from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.username


class Post(models.Model):
    text = models.TextField(blank=True, default="")
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self) -> str:
        return f"Post({self.id}) by {self.author_id}"
    

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    duration_days = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class ActionItem(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} ({'done' if self.done else 'open'})"
