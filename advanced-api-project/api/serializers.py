from rest_framework import serializers
from .models import Author, Book
from datetime import date

# BookSerializer handles validation for publication_year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer includes nested books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # nested serializer

    class Meta:
        model = Author
        fields = ['name', 'books']
