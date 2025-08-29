# accounts/urls.py
from django.urls import path
from .views import FollowUserView, UnfollowUserView, FollowingListView, FollowersListView

urlpatterns = [
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow-user"),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow-user"),
    path("<int:user_id>/following/", FollowingListView.as_view(), name="user-following"),
    path("<int:user_id>/followers/", FollowersListView.as_view(), name="user-followers"),
]
