from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Comment

User = get_user_model()

class PostsCommentsAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass1234")
        self.user2 = User.objects.create_user(username="bob", password="pass1234")
        self.post1 = Post.objects.create(author=self.user1, title="Hello", content="World")

    def auth(self, user):
        self.client.logout()
        self.client.login(username=user.username, password="pass1234")

    def test_create_post_requires_auth(self):
        url = "/api/posts/"
        res = self.client.post(url, {"title": "New", "content": "Post"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.auth(self.user1)
        res = self.client.post(url, {"title": "New", "content": "Post"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["author"]["username"], "alice")

    def test_update_delete_only_owner(self):
        url = f"/api/posts/{self.post1.id}/"
        self.auth(self.user2)
        res = self.client.patch(url, {"title": "Hack"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.auth(self.user1)
        res = self.client.patch(url, {"title": "Updated"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Updated")

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_comments_crud(self):
        self.auth(self.user2)
        # create
        res = self.client.post("/api/comments/", {"post": self.post1.id, "content": "Nice!"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment_id = res.data["id"]

        # list, filter by post
        res = self.client.get(f"/api/comments/?post={self.post1.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data["results"]) >= 1)

        # non-owner cannot update/delete
        self.auth(self.user1)
        res = self.client.patch(f"/api/comments/{comment_id}/", {"content": "Edit"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # owner can update/delete
        self.auth(self.user2)
        res = self.client.patch(f"/api/comments/{comment_id}/", {"content": "Edited"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.delete(f"/api/comments/{comment_id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_posts(self):
        Post.objects.create(author=self.user1, title="Django Tips", content="Rest Framework")
        res = self.client.get("/api/posts/?search=Tips")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Django Tips" == p["title"] for p in res.data["results"]))
