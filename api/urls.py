from django.urls import path
from api import views

urlpatterns = [
    path("books/", views.BookList.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book-detail"),
    path("books/create/", views.BookCreate.as_view(), name="book-create"),
    path("books/update/<int:pk>/", views.BookUpdate.as_view(), name="book-update"),
    path("books/delete/<int:pk>/", views.BookDelete.as_view(), name="book-delete"),
    path("authors/create/", views.AuthorCreate.as_view(), name="authors-create"),
    path("authors/", views.AuthorList.as_view(), name="author-list"),
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name="author-detail"),
]
