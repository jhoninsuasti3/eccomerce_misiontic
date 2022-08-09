from marketApp.models.detalle import Detalle
from rest_framework import serializers
from marketApp.models.producto import Producto
from marketApp.serializers.productoSerializer import ProductoSerializer
from marketApp.models.compra import Compra

class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle
        fields = ['cantidad', 'producto', 'compra']

    def create(self, request):
        producto = request['producto']
        compra = request['compra']
        cantidad = request['cantidad']
        precioUnidad = producto.precio
        precioTotal = precioUnidad * cantidad
        compra.total = compra.total + precioTotal
        compra.save()
        print(".....................................")
        print(compra.total)
        print(".....................................")
        detalle = Detalle.objects.create(cantidad = cantidad, precioTotal = precioTotal, compra = compra, producto = producto, precioUnidad = producto.precio)
        return detalle

    def to_representation(obj):
        print(".....................................")
        print(obj)
        print("......................................")
        return {
            'producto' : obj.producto.nombre,
            'cantidad' : obj.cantidad,
            'precioUnidad' : obj.precioUnidad,
            'precioTotal' : obj.precioTotal
        }