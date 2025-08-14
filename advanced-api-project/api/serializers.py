from rest_framework import serializers
from .models import Author, Book
from datetime import date

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation: publication_year cannot be in the future
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Serializer for the Author model
# Includes a nested BookSerializer to serialize all related books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # nested serializer for one-to-many relationship

    class Meta:
        model = Author
        fields = ['name', 'books']
