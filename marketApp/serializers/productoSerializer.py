from marketApp.models.producto import Producto
from rest_framework import serializers

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['precio', 'fabricante', 'detalleProducto', 'categoria']