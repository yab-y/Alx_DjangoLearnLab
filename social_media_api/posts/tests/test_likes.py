from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')
        self.post = Post.objects.create(author=self.user2, content='hello')
        self.client = APIClient()

    def test_like_post_creates_like_and_notification(self):
        self.client.login(username='u1', password='pass')
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())
        # Notification created for user2 (post.author)
        self.assertTrue(Notification.objects.filter(recipient=self.user2, actor=self.user1, verb__icontains='liked').exists())

    def test_unlike_removes_like_and_notification(self):
        # first like
        self.client.login(username='u1', password='pass')
        like_url = reverse('post-like', kwargs={'pk': self.post.pk})
        self.client.post(like_url)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())
        # now unlike
        unlike_url = reverse('post-unlike', kwargs={'pk': self.post.pk})
        resp = self.client.post(unlike_url)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Like.objects.filter(user=self.user1, post=self.post).exists())
        # notification should be removed
        self.assertFalse(Notification.objects.filter(recipient=self.post.author, actor=self.user1, verb__icontains='liked').exists())
