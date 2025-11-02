from django.contrib import admin
from .models import Producto, Categoria, Etiqueta, DetalleProductos
admin.site.register([Producto, Categoria, Etiqueta, DetalleProductos])