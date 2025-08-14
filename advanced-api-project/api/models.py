from django.db import models
from datetime import date

# Author model represents a book author
class Author(models.Model):
    name = models.CharField(max_length=100)  # store the author's name

    def __str__(self):
        return self.name

# Book model represents a book with a link to its author
class Book(models.Model):
    title = models.CharField(max_length=200)            # book title
    publication_year = models.IntegerField()            # year of publication
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)  # one-to-many relationship

    def __str__(self):
        return self.title
