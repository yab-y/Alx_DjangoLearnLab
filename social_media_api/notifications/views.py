from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        if pk:
            notif = Notification.objects.filter(pk=pk, recipient=request.user).first()
            if not notif:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            notif.unread = False
            notif.save()
            return Response({'detail': 'marked read'}, status=status.HTTP_200_OK)
        else:
            Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
            return Response({'detail': 'all marked read'}, status=status.HTTP_200_OK)
