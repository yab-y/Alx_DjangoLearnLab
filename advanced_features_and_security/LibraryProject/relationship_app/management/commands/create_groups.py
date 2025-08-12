from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

class Command(BaseCommand):
    help = "Create user groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Get content type for Book
        book_ct = ContentType.objects.get_for_model(Book)

        # Define permissions
        can_view = Permission.objects.get(codename='can_view', content_type=book_ct)
        can_create = Permission.objects.get(codename='can_create', content_type=book_ct)
        can_edit = Permission.objects.get(codename='can_edit', content_type=book_ct)
        can_delete = Permission.objects.get(codename='can_delete', content_type=book_ct)

        # Create groups
        groups_permissions = {
            "Viewers": [can_view],
            "Editors": [can_view, can_create, can_edit],
            "Admins": [can_view, can_create, can_edit, can_delete],
        }

        for group_name, perms in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set(perms)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' created/updated."))

