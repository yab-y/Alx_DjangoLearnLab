from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create the router and register the ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Old ListAPIView endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # Include router-generated URLs (CRUD for books_all)
    path('', include(router.urls)),
]
