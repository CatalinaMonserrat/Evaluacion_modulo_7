from django.db import models
from django.core.validators import MinValueValidator #Valida que el precio sea mayor a 0

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre
    
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)

    # Relaciones
    #Muchos a Uno: Varios productos a 1 categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, #Evita que se borre la categoria si se tiene productos
        related_name='productos')

    #Muchos a Muchos: Varios productos a muchos etiquetas
    etiquetas = models.ManyToManyField(Etiqueta, related_name='productos', blank=True)

    class Meta:
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre', 'precio'])
        ]
    def __str__(self):
        return self.nombre
    
class DetalleProductos(models.Model):
    #Uno a Uno: cada producto tiene un detalle unico
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='detalle')
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True, validators=[MinValueValidator(0)])
    alto_cm = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True, validators=[MinValueValidator(0)])
    ancho_cm = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True, validators=[MinValueValidator(0)])
    largo_cm = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Detalles de {self.producto.nombre}"
