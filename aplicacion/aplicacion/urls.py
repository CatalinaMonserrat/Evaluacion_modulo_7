from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('productos.urls')),  # tu app principal
    path('accounts/', include('django.contrib.auth.urls')),  
    path('admin/', admin.site.urls),
]