from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Etiqueta, DetalleProductos

def index(request):
    return render(request, 'index.html')

def lista_productos(request):
    productos = Producto.objects.all(). order_by('-id')
    return render(request, 'productos/lista.html'), {'productos': productos}

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'productos/detalle.html', {'producto': producto})

