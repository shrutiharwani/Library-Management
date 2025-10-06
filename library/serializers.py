from rest_framework import serializers
from .models import Book, CartItem, IssuedBook, SavedBook

class BookSerializer(serializers.ModelSerializer):
    issued_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'price', 'cover_image', 'total_copies', 'available_copies', 'issued_count']


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity', 'added_at']


class IssueSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = IssuedBook
        fields = ['id', 'book', 'issue_date', 'return_date', 'returned']


class SavedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = SavedBook
        fields = ['id', 'book', 'saved_at']
