from django.urls import path

from api import views
from api.views import OrderView, OrderCallbackView, OrdersViewSet

urlpatterns = [
    path("", views.all_links, name="all-links"),
    path("books/", views.BookList.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book-detail"),
    path("books/create/", views.BookCreate.as_view(), name="book-create"),
    path("books/update/<int:pk>/", views.BookUpdate.as_view(), name="book-update"),
    path("books/delete/<int:pk>/", views.BookDelete.as_view(), name="book-delete"),
    path("authors/create/", views.AuthorCreate.as_view(), name="authors-create"),
    path("authors/", views.AuthorList.as_view(), name="author-list"),
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name="author-detail"),
    path(
        "authors/update/<int:pk>/", views.AuthorUpdate.as_view(), name="author-update"
    ),
    path(
        "authors/delete/<int:pk>/", views.AuthorDelete.as_view(), name="author-delete"
    ),
    path("users/register/", views.UserRegistrationView.as_view(), name="user-register"),
    path(
        "users/token/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("order/", OrderView.as_view()),
    path("monobank/callback", OrderCallbackView.as_view(), name="mono_callback"),
    path("orders/", OrdersViewSet.as_view({"get": "list"})),
]
