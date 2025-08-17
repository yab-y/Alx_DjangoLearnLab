from django.urls import path
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
]
