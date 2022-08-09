from django.db import models
from .producto import Producto
from .compra import Compra

class Detalle(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(default=0)
    precioUnidad = models.FloatField(default=0)
    precioTotal = models.FloatField(default=0)
    producto = models.ForeignKey(Producto, related_name='producto', on_delete=models.CASCADE, default=1)
    compra =  models.ForeignKey(Compra, related_name='factura', on_delete=models.CASCADE, default=1)