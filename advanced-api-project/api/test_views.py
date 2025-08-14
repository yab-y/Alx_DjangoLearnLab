from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book, Author


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.staff_user = User.objects.create_user(username="staffuser", password="staffpass", is_staff=True)

        # Create authors
        self.author_a = Author.objects.create(name="Author A")
        self.author_b = Author.objects.create(name="Author B")

        # Create books
        self.book1 = Book.objects.create(
            title="Book One",
            author=self.author_a,
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author=self.author_b,
            publication_year=2021
        )

        # URLs
        self.list_url = reverse('book-list')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.create_url = reverse('book-create')
        self.update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})

    # -----------------------------
    # LIST & DETAIL TESTS
    # -----------------------------
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_book_detail(self):
        response = self.client.get(self.detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # -----------------------------
    # CREATE TESTS
    # -----------------------------
    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "title": "Book Three",
            "author": self.author_a.pk,
            "publication_year": 2022
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "Book Four",
            "author": self.author_a.pk,
            "publication_year": 2023
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # UPDATE TESTS
    # -----------------------------
    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "title": "Book One Updated",
            "author": self.author_a.pk,
            "publication_year": 2020
        }
        response = self.client.put(self.update_url(self.book1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Book One Updated")

    def test_update_book_unauthenticated(self):
        data = {
            "title": "Unauthorized Update",
            "author": self.author_a.pk,
            "publication_year": 2020
        }
        response = self.client.put(self.update_url(self.book1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # DELETE TESTS
    # -----------------------------
    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # FILTERING, SEARCH, ORDERING
    # -----------------------------
    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url, {'title': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_order_books_by_publication_year_desc(self):
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)
