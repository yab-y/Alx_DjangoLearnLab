# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class CustomUserManager(BaseUserManager):
    """
    Manager for CustomUser. Uses email as unique identifier if desired.
    """

    def create_user(self, username, email=None, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        """
        Create and save a regular user with the given username and password.
        """
        if not username:
            raise ValueError("The username field is required")
        email = self.normalize_email(email) if email else None
        user = self.model(
            username=username,
            email=email,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        """
        Create and save a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )


def user_profile_photo_upload_to(instance, filename):
    # Optional: store uploads by user id and timestamp to avoid name clashes
    ts = timezone.now().strftime("%Y%m%d%H%M%S")
    return f"profile_photos/user_{instance.id or 'new'}_{ts}_{filename}"


class CustomUser(AbstractUser):
    """
    Extend AbstractUser to add date_of_birth and profile_photo
    Keep username field for compatibility; you can switch to email-based login if you want.
    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to=user_profile_photo_upload_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.get_username()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
