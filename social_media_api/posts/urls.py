# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, PostLikeToggle, PostUnlike

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
     path('posts/<int:pk>/like/', PostLikeToggle.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', PostUnlike.as_view(), name='post-unlike'),
]
