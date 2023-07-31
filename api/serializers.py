from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Author, Book, Order


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token if needed
        # For example, you can add the user's email to the token
        token["email"] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional data to the response if needed
        # For example, you can add the user's email to the response
        data["email"] = self.user.email

        return data


class OrderContentSerializer(serializers.Serializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    order = OrderContentSerializer(many=True, allow_empty=False)


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["total_price", "created_at", "invoice_id", "id", "books", "status"]


class MonoCallbackSerializer(serializers.Serializer):
    invoiceId = serializers.CharField()
    status = serializers.CharField()
    amount = serializers.IntegerField()
    ccy = serializers.IntegerField()
    reference = serializers.CharField()
