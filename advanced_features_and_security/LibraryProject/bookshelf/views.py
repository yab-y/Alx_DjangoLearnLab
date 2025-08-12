from django.shortcuts import render
from .models import Book
from .forms import SearchForm
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def book_search(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.none()

    if form.is_valid():
        query = form.cleaned_data['query']
        # Safe ORM query prevents SQL injection
        books = Book.objects.filter(title__icontains=query)

    return render(request, 'bookshelf/book_search.html', {'form': form, 'books': books})
