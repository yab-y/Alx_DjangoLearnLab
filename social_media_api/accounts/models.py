# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Users this user follows
    # symmetrical=False because follow is directional (A follows B != B follows A)
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
        help_text="The users that this user follows."
    )

    def follow(self, user):
        """Follow a user (no-op if already following)."""
        if user == self:
            return
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow a user (no-op if not following)."""
        if user == self:
            return
        self.following.remove(user)

    def is_following(self, user) -> bool:
        return self.following.filter(pk=user.pk).exists()

    def __str__(self):
        return self.username
