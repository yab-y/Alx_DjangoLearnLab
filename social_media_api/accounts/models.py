from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, default="")
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    # Followers: many-to-many to self, asymmetrical (A can follow B without B following A)
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True
    )

    def __str__(self):
        return self.username
