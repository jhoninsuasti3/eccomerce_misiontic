from rest_framework import serializers
from marketApp.models.user import User
from marketApp.models.compra import Compra

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'rol']
    
    def create(self, validated_data):
        userInstance = User.objects.create(**validated_data)
        return userInstance

    def to_representation(self, obj):
        print(".....................................9")
        print(obj)
        print(".....................................<.")
        user = User.objects.get(id=obj.id)
        compra = Compra.objects.filter(client_id=user.id)
        ultimaCompra = 1
        for comp in compra:
            if ultimaCompra < comp.id:
                ultimaCompra = comp.id

        return {
            'userna': user.username,
            'id' : user.id,
            'compraActual': ultimaCompra
        }