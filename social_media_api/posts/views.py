# posts/views.py  (append or merge with your existing file)
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer
from .pagination import DefaultPagination

User = get_user_model()

class FeedView(generics.ListAPIView):
    """
    Returns posts from users that the current authenticated user follows.
    GET /api/posts/feed/
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        # if user follows nobody, this will be empty
        following_qs = user.following.all()
        return Post.objects.filter(author__in=following_qs).order_by("-created_at")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx
