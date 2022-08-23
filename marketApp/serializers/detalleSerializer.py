from rest_framework import serializers
from marketApp.models.detalle import Detalle
from marketApp.models.producto import Producto
from marketApp.models.compra import Compra
from marketApp.serializers.productoSerializer import ProductoSerializer

class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle
        fields = ['cantidad', 'producto', 'compra']

    def create(self, validated_data):
        producto = validated_data['producto']
        compra = validated_data['compra']
        cantidad = validated_data['cantidad']
        precioUnidad = producto.precio
        precioTotal = precioUnidad * cantidad
        compra.total = compra.total + precioTotal
        compra.save()
        detalle = Detalle.objects.create(cantidad = cantidad, precioTotal = precioTotal, compra = compra, producto = producto, precioUnidad = producto.precio)
        detalle.save()
        return detalle

    def crearRespuesta(*args, **kwargs):
        idCliente = kwargs['clave']
        detalle = Detalle.objects.get(id=kwargs['detalle'])
        compra = detalle.compra
        user = compra.client
        if kwargs['clave'] != user.id :
            return {
                'detail':'Unauthorized Request'
            }

        return {
            'id' : detalle.id,
            'producto' : detalle.producto.nombre,
            'cantidad' : detalle.cantidad,
            'precioUnidad' : detalle.precioUnidad,
            'precioTotal' : detalle.precioTotal,
            'compraId' :compra.id
        }

    def respuesta(obj):
        return {
            'id' : obj.id,
            'producto' : obj.producto.nombre,
            'cantidad' : obj.cantidad,
            'precioUnidad' : obj.precioUnidad,
            'precioTotal' : obj.precioTotal
        }

    def actualizar(request, *args, **kwargs):
        idCliente = kwargs['clave']
        detalle = Detalle.objects.get(id=kwargs['detalle'])
        compra = detalle.compra
        compra.total = compra.total - detalle.precioTotal
        user = compra.client
        if kwargs['clave'] != user.id :
            return {
                'detail':'Unauthorized Request'
            }

        producto = detalle.producto
        cambios = request.data
        for key in cambios:
            if key == 'producto':
                producto = Producto.objects.get(id=cambios[key])
                detalle.producto = producto
            
            if key == 'cantidad':
                detalle.cantidad = cambios[key]

        detalle.precioUnidad = producto.precio
        detalle.precioTotal = detalle.precioUnidad * detalle.cantidad
        compra.total = compra.total + detalle.precioTotal
        compra.save()
        detalle.save()
        return {
                'estado':'ok'
            }

    def eliminar(*args, **kwargs):
        idCliente = kwargs['clave']
        detalle = Detalle.objects.get(id=kwargs['detalle'])
        compra = detalle.compra
        compra.total = compra.total - detalle.precioTotal
        compra.save()
        user = compra.client
        if kwargs['clave'] != user.id :
            return {
                'detail':'Unauthorized Request'
            }
        
        detalle.delete()
        return {
                'estado':'ok'
            }