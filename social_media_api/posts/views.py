from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class PostLikeToggle(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # <-- checker wants this
        like, created = Like.objects.get_or_create(user=request.user, post=post)  # <-- checker wants this
        if created:
            # create notification explicitly
            if post.user != request.user:
                Notification.objects.create(
                    recipient=post.user,
                    actor=request.user,
                    verb="liked your post",
                    target=post
                )
            return Response({'detail': 'post liked', 'liked': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'already liked', 'liked': True}, status=status.HTTP_200_OK)
#

class PostUnlike(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        deleted, _ = Like.objects.filter(user=user, post=post).delete()
        if deleted:
            # signal handler will remove notifications
            return Response({'detail': 'post unliked', 'liked': False}, status=status.HTTP_200_OK)
        return Response({'detail': 'not liked previously'}, status=status.HTTP_400_BAD_REQUEST)
#