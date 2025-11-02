from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Producto, Categoria, Etiqueta, DetalleProductos
from .forms import ProductoForm, CategoriaForm, EtiquetaForm


def index(request):
    return render(request, 'index.html')


# =================== Productos ===================

def lista_productos(request):
    q = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')

    productos = (
        Producto.objects
        .select_related('categoria')
        .all()
        .order_by('-id')
    )

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.order_by('nombre')

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

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.save()
            form.save_m2m()

            DetalleProductos.objects.update_or_create(
                producto=p,
                defaults={
                    'peso_kg':  form.cleaned_data.get('peso_kg')  or None,
                    'alto_cm':  form.cleaned_data.get('alto_cm')  or None,
                    'ancho_cm': form.cleaned_data.get('ancho_cm') or None,
                    'largo_cm': form.cleaned_data.get('largo_cm') or None,
                },
            )
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('detalle_producto', id=p.id)
    else:
        form = ProductoForm()
    return render(request, 'productos/crear.html', {'form': form})


@login_required
def editar_producto(request, id):
    p = get_object_or_404(Producto, pk=id)

    inicial = {}
    # OJO: related_name='detalle' → acceso como p.detalle
    d = getattr(p, 'detalle', None)
    if d:
        inicial = {
            'peso_kg':  d.peso_kg,
            'alto_cm':  d.alto_cm,
            'ancho_cm': d.ancho_cm,
            'largo_cm': d.largo_cm,
        }

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=p)
        if form.is_valid():
            p = form.save()
            DetalleProductos.objects.update_or_create(
                producto=p,
                defaults={
                    'peso_kg':  form.cleaned_data.get('peso_kg')  or None,
                    'alto_cm':  form.cleaned_data.get('alto_cm')  or None,
                    'ancho_cm': form.cleaned_data.get('ancho_cm') or None,
                    'largo_cm': form.cleaned_data.get('largo_cm') or None,
                },
            )
            messages.success(request, 'Producto actualizado.')
            return redirect('detalle_producto', id=p.id)
    else:
        form = ProductoForm(instance=p, initial=inicial)

    return render(request, 'productos/editar.html', {'form': form, 'producto': p})

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})


# =================== Categorías ===================

def lista_categorias(request):
    categorias = Categoria.objects.order_by('nombre')
    return render(request, 'categorias/lista.html', {'categorias': categorias})


@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('lista_categorias')
        messages.error(request, 'Error al crear la categoría.')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear_categoria.html', {'form': form})


@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('lista_categorias')
        messages.error(request, 'Error al actualizar la categoría.')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/editar_categoria.html', {'form': form})


@login_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada exitosamente.')
        return redirect('lista_categorias')
    return render(request, 'categorias/eliminar_categoria.html', {'categoria': categoria})


# =================== Etiquetas ===================

def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.order_by('nombre')
    return render(request, 'etiquetas/lista.html', {'etiquetas': etiquetas})


@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta creada exitosamente.')
            return redirect('lista_etiquetas')
        messages.error(request, 'Error al crear la etiqueta.')
    else:
        form = EtiquetaForm()
    return render(request, 'etiquetas/crear_etiqueta.html', {'form': form})


@login_required
def editar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, pk=id)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta actualizada exitosamente.')
            return redirect('lista_etiquetas')
        messages.error(request, 'Error al actualizar la etiqueta.')
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, 'etiquetas/editar_etiqueta.html', {'form': form, 'etiqueta': etiqueta})


@login_required
def eliminar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, pk=id)
    if request.method == 'POST':
        nombre = etiqueta.nombre
        etiqueta.delete()
        messages.success(request, f'Etiqueta "{nombre}" eliminada exitosamente.')
        return redirect('lista_etiquetas')
    return render(request, 'etiquetas/eliminar_etiqueta.html', {'etiqueta': etiqueta})
