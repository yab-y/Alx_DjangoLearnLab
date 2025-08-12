# relationship_app/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = [
         ('admin', 'Admin'),
         ('editor', 'Editor'),
         ('viewer', 'Viewer'),
    ]
class Book(models.Model):
    # your existing fields here, for example:
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    # other fields...

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Signal to create UserProfile automatically when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Member')  # Default role

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
