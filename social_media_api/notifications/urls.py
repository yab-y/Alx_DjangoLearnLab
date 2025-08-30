from django.urls import path
from .views import NotificationListView, NotificationMarkReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/mark-read/', NotificationMarkReadView.as_view(), name='notifications-mark-all-read'),
    path('notifications/<int:pk>/mark-read/', NotificationMarkReadView.as_view(), name='notifications-mark-read'),
]
