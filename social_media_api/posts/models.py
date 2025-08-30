from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# import your existing Post model
# from .models import Post  # If Post is in the same file adjust accordingly
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    # Example minimal Post; replace with your real Post model fields
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.pk} by {self.author}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} liked Post {self.post_id}"
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.post.id}"