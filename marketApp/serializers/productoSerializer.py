from rest_framework import serializers
from marketApp.models.detalle import Detalle
from marketApp.models.producto import Producto
from marketApp.models.compra import Compra
from marketApp.models.user import User

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['precio', 'fabricante', 'detalleProducto', 'categoria', 'nombre']

    def agregar(obj, **kwargs):
        usuario = User.objects.get(id=kwargs['proveedor'])
        return {
            'precio' : obj['precio'],
            'fabricante' : usuario,
            'detalleProducto' : obj['detalleProducto'],
            'categoria' : obj['categoria'],
            'nombre' : obj['nombre']
        }

    def crear(self, validated_data, *args, **kwargs):
        usuario = User.objects.get(id=kwargs['user'])
        if usuario.rol == 'admin':
            datos = ProductoSerializer.agregar(validated_data.data, proveedor=validated_data.data['fabricante'])
        elif usuario.rol == 'proveedor':
            datos = ProductoSerializer.agregar(validated_data.data, proveedor=kwargs['user'])
        else:
            return None
        userInstance = Producto.objects.create(**datos)
        return userInstance

    def crearRespuesta(*args, **kwargs):
        producto = Producto.objects.get(id=kwargs['producto'])
        
        return {
            'precio' : producto.precio,
            'fabricante' : producto.fabricante.name,
            'detalleProducto' : producto.detalleProducto,
            'categoria' : producto.categoria,
            'nombre' : producto.nombre
        }

    def actualizar(request, *args, **kwargs):
        usuario = User.objects.get(id=kwargs['clave'])
        producto = Producto.objects.get(id=kwargs['producto'])
        if usuario.rol == 'proveedor':
            if usuario.id != producto.fabricante.id:
                return None 
        elif usuario.rol != 'admin':
            return None   

        cambios = request.data
        for key in cambios:
            if key == 'precio':
                producto.precio = cambios[key]
            if key == 'nombre':
                producto.nombre = cambios[key]
            if key == 'detalleProducto':
                producto.detalleProducto = cambios[key]
            if key == 'categoria':
                producto.categoria = cambios[key]
            if (key == 'fabricante') and (usuario.rol == 'admin'):
                proveedor = User.objects.get(id=cambios[key])
                producto.fabricante = proveedor

        producto.save()
        return {
                'estado':'ok'
            }

    def eliminar(*args, **kwargs):
        usuario = User.objects.get(id=kwargs['clave'])
        producto = Producto.objects.get(id=kwargs['producto'])
        if usuario.rol == 'proveedor':
            if usuario.id != producto.fabricante.id:
                return None 
        elif usuario.rol != 'admin':
            return None   
        
        producto.delete()
        return {
                'estado':'ok'
            }