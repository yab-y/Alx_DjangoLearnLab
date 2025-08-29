from django.test import TestCase

# Create your tests here.
# accounts/tests.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class FollowAPITests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="pass")
        self.bob = User.objects.create_user(username="bob", password="pass")

    def test_follow_unfollow(self):
        # unauthenticated cannot follow
        res = self.client.post(f"/api/accounts/follow/{self.bob.id}/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticate as alice
        self.client.login(username="alice", password="pass")

        # follow
        res = self.client.post(f"/api/accounts/follow/{self.bob.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.alice.refresh_from_db()
        self.assertTrue(self.alice.is_following(self.bob))
        self.assertTrue(self.bob.followers.filter(pk=self.alice.pk).exists())

        # unfollow
        res = self.client.post(f"/api/accounts/unfollow/{self.bob.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.alice.refresh_from_db()
        self.assertFalse(self.alice.is_following(self.bob))
