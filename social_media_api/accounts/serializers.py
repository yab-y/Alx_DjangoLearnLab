# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTinySerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "followers_count", "following_count", "is_following")

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.is_following(obj)
