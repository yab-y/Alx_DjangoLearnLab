from django.urls import path
from .views import search_posts
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Post URLs
    path('post/', PostListView.as_view(), name='post-list'),                 # list all posts
    path('post/new/', PostCreateView.as_view(), name='post-create'),         # create a post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),    # view a single post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # edit post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # delete post
    path('search/', search_posts, name='search-posts'),
    path('tags/<slug:tag_name>/', posts_by_tag, name='posts-by-tag'),
    # Comment URLs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),  # add comment
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),     # edit comment
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),     # delete comment
]
