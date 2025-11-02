from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction, IntegrityError
from .models import Producto, Categoria, Etiqueta
from .forms import ProductoForm, CategoriaForm, EtiquetaForm

def index(request):
    return render(request, 'index.html')

# ==============  Views para productos ===============

def lista_productos(request):
    q = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    productos = Producto.objects.select_related('categoria').all().order_by('-id')

    if q:
        from django.db.models import Q
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all().order_by('nombre')
    ctx = {
        'productos': productos,
        'q': q,
        'categoria_id': categoria_id,
        'categorias': categorias,
    }
    return render(request, 'productos/lista.html', ctx)

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    return render(request, 'productos/detalle.html', {'producto': producto})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    p = form.save()
                messages.success(request, 'Producto creado exitosamente.')
                return redirect('detalle_producto', id=p.id)
            except IntegrityError:
                form.add_error(None, 'Ya existe un producto con el mismo nombre.')
        else:
            messages.error(request, 'Error al crear el producto.')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear.html', {'form': form})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            p = form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('detalle_producto', id=p.id)
        else:
            messages.error(request, 'Error al actualizar el producto.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
        return redirect('lista_productos')
    else:
        return render(request, 'productos/eliminar.html', {'producto': producto})
    
# ==============  Views para categorias ===============

def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'categorias/lista.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Error al crear la categoría.')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear_categoria.html', {'form': form})

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Error al actualizar la categoría.')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/editar_categoria.html', {'form': form})

def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada exitosamente.')
        return redirect('lista_categorias')
    else:
        return render(request, 'categorias/eliminar_categoria.html', {'categoria': categoria})


# ==============  Views para categorias ===============

def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.all().order_by('nombre')
    return render(request, 'etiquetas/lista.html', {'etiquetas': etiquetas})

def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta creada exitosamente.')
            return redirect('lista_etiquetas')
        else:
            messages.error(request, 'Error al crear la etiqueta.')
    else:
        form = EtiquetaForm()
    return render(request, 'etiquetas/crear_etiqueta.html', {'form': form})

def editar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, pk=id)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta actualizada exitosamente.')
            return redirect('lista_etiquetas')
        else:
            messages.error(request, 'Error al actualizar la etiqueta.')
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, 'etiquetas/editar_etiqueta.html', {'form': form, 'etiqueta': etiqueta})

def eliminar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, pk=id)
    if request.method == 'POST':
        nombre = etiqueta.nombre
        etiqueta.delete()
        messages.success(request, f'Etiqueta "{nombre}" eliminada exitosamente.')
        return redirect('lista_etiquetas')
    else:
        return render(request, 'etiquetas/eliminar_etiqueta.html', {'etiqueta': etiqueta})