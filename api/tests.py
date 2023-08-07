import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from api.models import Book, Author


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def access_token(user):
    return AccessToken.for_user(user)


@pytest.fixture
def authenticated_client(api_client, access_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def author():
    return Author.objects.create(name="John Doe")


@pytest.fixture
def book(author):
    return Book.objects.create(
        title="Book 1",
        author=author,
        genre="Fiction",
        publication_date="2022-01-01",
        price=1000,
        quantity=10,
    )


@pytest.mark.django_db
class TestBookAPIViews:
    def test_get_all_books(self, authenticated_client, book):
        url = reverse("book-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_book_by_id(self, authenticated_client, book):
        url = reverse("book-detail", kwargs={"pk": book.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Book 1"

    def test_update_book(self, authenticated_client, book):
        url = reverse("book-update", kwargs={"pk": book.pk})
        data = {
            "title": "Updated Book",
            "genre": "Mystery",
            "publication_date": "2022-01-01",
            "author": book.author.id,
            "price": 1000,
            "quantity": 10,
        }
        response = authenticated_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Book.objects.get(pk=book.pk).title == "Updated Book"
        assert Book.objects.get(pk=book.pk).genre == "Mystery"

    def test_create_book(self, authenticated_client, author):
        url = reverse("book-create")
        data = {
            "title": "Book 2",
            "author": author.id,
            "genre": "Fantasy",
            "publication_date": "2023-06-01",
            "price": 1000,
            "quantity": 10,
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == 1
        assert Book.objects.get(title="Book 2").genre == "Fantasy"

    def test_delete_book(self, authenticated_client, book):
        url = reverse("book-delete", kwargs={"pk": book.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.count() == 0


@pytest.mark.django_db
class TestAuthorAPIViews:
    def test_get_all_authors(self, authenticated_client, author):
        url = reverse("author-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_author_by_id(self, authenticated_client, author):
        url = reverse("author-detail", kwargs={"pk": author.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "John Doe"

    def test_update_author(self, authenticated_client, author):
        url = reverse("author-update", kwargs={"pk": author.pk})
        data = {
            "name": "Jane Doe",
        }
        response = authenticated_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Author.objects.get(pk=author.pk).name == "Jane Doe"

    def test_create_author(self, authenticated_client):
        url = reverse("authors-create")
        data = {
            "name": "Jane Doe",
        }
        response = authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.count() == 1
        assert Author.objects.get(name="Jane Doe").name == "Jane Doe"

    def test_delete_author(self, authenticated_client, author):
        url = reverse("author-delete", kwargs={"pk": author.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Author.objects.count() == 0
