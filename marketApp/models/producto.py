from django.db import models
from .user import User

class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    precio = models.IntegerField(default=0)
    nombre = models.CharField('NombreProducto', max_length = 300, default="generic")
    fabricante = models.ForeignKey(User, related_name='fabricante', on_delete=models.CASCADE)
    detalleProducto = models.CharField('DetalleProducto', max_length = 300)
    categoria = models.CharField('Categoria', max_length = 100)
