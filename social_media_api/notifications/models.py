from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)  # e.g. "liked your post"
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification to {self.recipient}: {self.actor} {self.verb}"
