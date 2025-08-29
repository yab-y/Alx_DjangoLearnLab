# accounts/views.py
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserTinySerializer

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = generics.get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target)
        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = generics.get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.unfollow(target)
        return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    """
    List users that <user_id> is following.
    """
    serializer_class = UserTinySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # optional: or reuse DefaultPagination

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = generics.get_object_or_404(User, pk=user_id)
        return user.following.all()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class FollowersListView(generics.ListAPIView):
    """
    List users that follow <user_id>.
    """
    serializer_class = UserTinySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = generics.get_object_or_404(User, pk=user_id)
        return user.followers.all()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx
