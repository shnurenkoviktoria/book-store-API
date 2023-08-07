from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Author, Book, Order, MonoSettings, OrderItem
from api.mono import create_order, verify_signature
from api.permissions import IsAuthenticatedOrReadOnly
from api.serializers import (
    AuthorSerializer,
    BookSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    OrderModelSerializer,
    OrderSerializer,
    MonoCallbackSerializer,
)
from django.shortcuts import render


def home(request):
    return render(request, 'urls_page.html')


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class AuthorList(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        queryset = Author.objects.all()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class AuthorCreate(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDetail(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorUpdate(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDelete(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        queryset = Book.objects.all()
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        genre = self.request.query_params.get("genre")
        publication_date = self.request.query_params.get("publication_date")
        price = self.request.query_params.get("price")
        quantity = self.request.query_params.get("quantity")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__name__icontains=author)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if publication_date:
            queryset = queryset.filter(publication_date__icontains=publication_date)
        if price:
            queryset = queryset.filter(price__icontains=price)
        if quantity:
            queryset = queryset.filter(quantity__icontains=quantity)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreate(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookUpdate(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDelete(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrdersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderModelSerializer
    permission_classes = [permissions.AllowAny]


class OrderView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order = OrderSerializer(data=request.data)
        order.is_valid(raise_exception=True)
        webhook_url = request.build_absolute_uri(reverse("mono_callback"))
        order_data = create_order(order.validated_data["order"], webhook_url)
        return Response(order_data)


class OrderCallbackView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        public_key = MonoSettings.get_token()
        if not verify_signature(
                public_key, request.headers.get("X-Sign"), request.body
        ):
            return Response({"status": "signature mismatch"}, status=400)
        callback = MonoCallbackSerializer(data=request.data)
        callback.is_valid(raise_exception=True)
        try:
            order = Order.objects.get(id=callback.validated_data["reference"])
        except Order.DoesNotExist:
            return Response({"status": "order not found"}, status=404)
        if order.invoice_id != callback.validated_data["invoiceId"]:
            return Response({"status": "invoiceId mismatch"}, status=400)
        order.status = callback.validated_data["status"]
        order.save()
        id_order = order.id
        id = OrderItem.objects.get(id=id_order)
        book = Book.objects.get(id=id.book_id)
        if (
                order.status == "failure"
                or order.status == "expired"
                or order.status == "reversed"
                or order.status == "hold"
        ):
            book.quantity += id.quantity
            book.save()

        return Response({"status": order.status})
