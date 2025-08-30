from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from django.urls import reverse

User = get_user_model()

class NotificationAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')
        self.post = Post.objects.create(author=self.user2, content='hello')
        self.client.login(username='u1', password='pass')

    def test_notifications_list(self):
        # user1 likes user2's post -> notification to user2
        Like.objects.create(user=self.user1, post=self.post)
        self.client.logout()
        self.client.login(username='u2', password='pass')
        url = reverse('notifications-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()) >= 1)
