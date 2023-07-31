from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from api.models import Author, Book


class BookTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Book 1",
            author=self.author,
            genre="Fiction",
            publication_date="2022-01-01",
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_all_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_by_id(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book 1")

    def test_update_book(self):
        url = reverse("book-update", kwargs={"pk": self.book.pk})
        data = {
            "title": "Updated Book",
            "genre": "Mystery",
            "publication_date": "2022-01-01",
            "author": self.author.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book.pk).title, "Updated Book")
        self.assertEqual(Book.objects.get(pk=self.book.pk).genre, "Mystery")

    def test_create_book(self):
        url = reverse("book-create")
        data = {
            "title": "Book 2",
            "author": self.author.id,
            "genre": "Fantasy",
            "publication_date": "2023-06-01",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(title="Book 2").genre, "Fantasy")

    def test_delete_book(self):
        url = reverse("book-delete", kwargs={"pk": self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_get_all_authors(self):
        url = reverse("author-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_author_by_id(self):
        url = reverse("author-detail", kwargs={"pk": self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Doe")

    def test_update_author(self):
        url = reverse("author-update", kwargs={"pk": self.author.pk})
        data = {
            "name": "Jane Doe",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get(pk=self.author.pk).name, "Jane Doe")

    def test_create_author(self):
        url = reverse("authors-create")
        data = {
            "name": "Jane Doe",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(Author.objects.get(name="Jane Doe").name, "Jane Doe")

    def test_delete_author(self):
        url = reverse("author-delete", kwargs={"pk": self.author.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)
