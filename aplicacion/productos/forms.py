from django import forms
from .models import Producto, Categoria, Etiqueta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'etiquetas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese una descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Ingrese el precio del producto'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Ingrese el stock del producto'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'etiquetas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la nueva categoría'}),
        }

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la nueva etiqueta'}),
        }