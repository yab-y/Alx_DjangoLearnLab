from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at", "updated_at", "author")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at", "updated_at")
    search_fields = ("content",)
    list_filter = ("created_at", "updated_at", "author")
