from django import forms
from .models import Producto, Categoria, Etiqueta

class ProductoForm(forms.ModelForm):
    # Campos extra del OneToOne (con nombres del modelo)
    peso_kg  = forms.DecimalField(required=False, min_value=0, max_digits=6, decimal_places=2, label='Peso (kg)',
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}))
    alto_cm  = forms.DecimalField(required=False, min_value=0, max_digits=6, decimal_places=2, label='Altura (cm)',
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}))
    ancho_cm = forms.DecimalField(required=False, min_value=0, max_digits=6, decimal_places=2, label='Ancho (cm)',
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}))
    largo_cm = forms.DecimalField(required=False, min_value=0, max_digits=6, decimal_places=2, label='Largo (cm)',
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}))

    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio', 'stock', 'categoria', 'etiquetas',
            # los extras del O2O pueden ir aquí sin problema
            'peso_kg', 'alto_cm', 'ancho_cm', 'largo_cm'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese una descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
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