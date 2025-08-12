from django.contrib import admin
from django.urls import path, include  # import both

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # include your app urls here
]
