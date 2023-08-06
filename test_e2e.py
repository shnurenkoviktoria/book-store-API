import unittest

import requests


def urls(end):
    return "https://cryptic-garden-19358-66c5851b2ced.herokuapp.com/api/" + end


class TestBookAPI(unittest.TestCase):
    def setUp(self):
        url = urls("books/create/")
        headers = {"Content-Type": "application/json"}
        self.data = {
            "title": "The Great Gatsby",
            "author": 1,
            "genre": "Classic",
            "publication_date": "1925-04-10",
            "price": "100.00",
            "quantity": 10,
        }
        self.response = requests.post(url, json=self.data, headers=headers)
        self.book_id = self.response.json()["id"]

    def delete(self):
        url = urls(f"books/delete/{self.book_id}/")
        requests.delete(url)

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
        headers = {"Content-Type": "application/json"}
        data = {
            "title": "The Great",
            "author": 1,
            "genre": "drama",
            "publication_date": "1925-04-10",
            "price": "100.00",
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
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")


class TestAuthorAPI(unittest.TestCase):
    def setUp(self):
        url = urls("authors/create/")
        headers = {"Content-Type": "application/json"}
        self.data = {
            "name": "F. Scott Fitzgerald",
        }
        self.response = requests.post(url, json=self.data, headers=headers)
        self.author_id = self.response.json()["id"]

    def delete(self):
        url = urls(f"authors/delete/{self.author_id}/")
        requests.delete(url)

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
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "F. Scott",
        }
        response = requests.put(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], data["name"])
        self.delete()

    def test_delete_author(self):
        url = urls(f"authors/delete/{self.author_id}/")
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")
