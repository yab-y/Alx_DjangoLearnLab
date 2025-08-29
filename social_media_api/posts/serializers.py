from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class UserTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class CommentSerializer(serializers.ModelSerializer):
    author = UserTinySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "content", "created_at", "updated_at")
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = UserTinySerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "comments_count",
        )
        read_only_fields = ("id", "author", "created_at", "updated_at", "comments_count")

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)
