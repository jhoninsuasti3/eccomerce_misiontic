from marketApp.models.compra import Compra
from rest_framework import serializers
from marketApp.models.user import User
from marketApp.models.compra import Compra
from marketApp.models.detalle import Detalle
from marketApp.models.producto import Producto
from marketApp.serializers.userSerializer import UserSerializer
from marketApp.serializers.detalleSerializer import DetalleSerializer

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['client']

    def to_representation(self, obj):
        user = User.objects.get(id=obj.id)
        compra = Compra.objects.filter(client_id=user.id)
        compraActual = compra[0]
        for comp in compra:
            if compraActual.id < comp.id:
                compraActual = comp

        detalles = Detalle.objects.filter(compra_id=compraActual.id)  
        detallesResponse = []
        for detalle in detalles:
            detallesResponse.append(DetalleSerializer.to_representation(detalle))
        
        return {
            'id': compraActual.id,
            'cliente': user.username,
            'productos':  detallesResponse,
            'total':compraActual.total,
            'email': user.email
        }