import unittest
import requests
import time


def urls(end):
    return "https://cryptic-garden-19358-66c5851b2ced.herokuapp.com/api/" + end


def auth():
    url = urls("users/token/")
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "test@test",
        "password": "test",
    }
    response = requests.post(url, json=data, headers=headers)
    token = response.json().get("access")
    return {"Authorization": f"Bearer {token}"}


class TestBookAPI(unittest.TestCase):
    def setUp(self):
        self.headers = auth()
        url = urls("books/create/")
        headers = {"Content-Type": "application/json", **self.headers}
        self.data = {
            "title": "The Great Gatsby",
            "author": 1,
            "genre": "Classic",
            "publication_date": "1925-04-10",
            "price": 100,
            "quantity": 10,
        }
        self.response = requests.post(url, json=self.data, headers=headers)
        self.book_id = self.response.json()["id"]

    def delete(self):
        url = urls(f"books/delete/{self.book_id}/")
        requests.delete(url, headers=self.headers)

    def test_create_book(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertTrue("id" in self.response.json())
        self.assertEqual(self.response.json()["title"], self.data["title"])
        self.assertEqual(self.response.json()["author"], self.data["author"])
        self.assertEqual(self.response.json()["genre"], self.data["genre"])
        self.assertEqual(
            self.response.json()["publication_date"], self.data["publication_date"]
        )
        self.assertEqual(self.response.json()["price"], self.data["price"])
        self.assertEqual(self.response.json()["quantity"], self.data["quantity"])
        self.delete()

    def test_get_book_list(self):
        url = urls("books/")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.delete()

    def test_get_book_detail(self):
        url = urls(f"books/{self.book_id}/")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.book_id)
        self.delete()

    def test_update_book(self):
        url = urls(f"books/update/{self.book_id}/")
        headers = {"Content-Type": "application/json", **self.headers}
        data = {
            "title": "The Great",
            "author": 1,
            "genre": "drama",
            "publication_date": "1925-04-10",
            "price": 100,
            "quantity": 10,
        }
        response = requests.put(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertEqual(response.json()["author"], data["author"])
        self.assertEqual(response.json()["genre"], data["genre"])
        self.assertEqual(
            response.json()["publication_date"], self.data["publication_date"]
        )
        self.assertEqual(response.json()["price"], data["price"])
        self.assertEqual(response.json()["quantity"], data["quantity"])
        self.delete()

    def test_delete_book(self):
        url = urls(f"books/delete/{self.book_id}/")
        response = requests.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")


class TestAuthorAPI(unittest.TestCase):
    def setUp(self):
        self.headers = auth()
        url = urls("authors/create/")
        create_author_headers = {"Content-Type": "application/json", **self.headers}
        self.data = {
            "name": f"F. Scott Fitzgerald",
        }
        self.response = requests.post(
            url, json=self.data, headers=create_author_headers
        )
        self.author_id = self.response.json().get("id")

    def delete(self):
        url = urls(f"authors/delete/{self.author_id}/")
        requests.delete(url, headers=self.headers)

    def test_create_author(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertTrue("id" in self.response.json())
        self.assertEqual(self.response.json()["name"], self.data["name"])
        self.delete()

    def test_get_author_list(self):
        url = urls("authors/")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.delete()

    def test_get_author_detail(self):
        url = urls(f"authors/{self.author_id}/")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.author_id)
        self.delete()

    def test_update_author(self):
        url = urls(f"authors/update/{self.author_id}/")
        headers = {"Content-Type": "application/json", **self.headers}
        data = {
            "name": "F. Scott",
        }
        response = requests.put(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], data["name"])
        self.delete()

    def test_delete_author(self):
        url = urls(f"authors/delete/{self.author_id}/")
        response = requests.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")


class TestUserAPI(unittest.TestCase):
    def test_create_user(self):
        url = urls("users/register/")
        create_user_headers = {"Content-Type": "application/json"}
        self.data = {
            "username": f"test@user{int(time.time())}",
            "password": "test",
        }
        self.response = requests.post(url, json=self.data, headers=create_user_headers)
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.json()["username"], self.data["username"])

    def test_token(self):
        url = urls("users/token/")
        data = {
            "username": "test@user",
            "password": "test",
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.json())
        self.assertTrue("refresh" in response.json())


class TestOrderAPI(unittest.TestCase):
    def setUp(self):
        self.headers = auth()
        url = urls("books/create/")
        create_book_headers = {"Content-Type": "application/json", **self.headers}
        self.data = {
            "title": "The Great Gatsby",
            "author": 1,
            "genre": "drama",
            "publication_date": "1925-04-10",
            "price": 100,
            "quantity": 10,
        }
        self.response = requests.post(url, json=self.data, headers=create_book_headers)
        self.book_id = self.response.json().get("id")

    def delete(self):
        url = urls(f"books/delete/{self.book_id}/")
        requests.delete(url, headers=self.headers)

    def test_create_order(self):
        url = urls("order/")
        create_order_headers = {"Content-Type": "application/json"}
        data = {"order": [{"book_id": self.book_id, "quantity": 4}]}

        response = requests.post(url, json=data, headers=create_order_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("id" in response.json())
        self.assertTrue("url" in response.json())
        self.delete()

    def test_get_order_list(self):
        url = urls("orders/")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        self.delete()
