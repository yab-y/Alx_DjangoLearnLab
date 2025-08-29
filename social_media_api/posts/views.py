from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import DefaultPagination

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Allow ?search=term to look in title and content
    search_fields = ["title", "content"]
    # Allow ?ordering=created_at or -created_at
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post", "post__author").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["post"]  # enables ?post=<post_id>
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["created_at"]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx
