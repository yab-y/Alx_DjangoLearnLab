from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from posts.models import Like, Post
from notifications.models import Notification

@receiver(post_save, sender=Like)
def create_notification_on_like(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    recipient = post.author
    actor = instance.user
    if recipient == actor:
        # don't notify when user likes their own post (optional)
        return

    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb='liked your post',
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=str(post.pk),
    )

@receiver(post_delete, sender=Like)
def remove_like_notification(sender, instance, **kwargs):
    post = instance.post
    recipient = post.author
    actor = instance.user
    # Try to remove the like notification; if you prefer to mark unread/read, change accordingly.
    Notification.objects.filter(
        recipient=recipient,
        actor=actor,
        verb='liked your post',
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=str(post.pk),
    ).delete()
