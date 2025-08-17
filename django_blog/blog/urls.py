from django.urls import 
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('post/', PostListView.as_view(), name='post-list'),               # list view
    path('post/new/', PostCreateView.as_view(), name='post-create'),       # create new post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # view post detail
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # edit post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # delete post
    path('post/<int:post_pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),


]
