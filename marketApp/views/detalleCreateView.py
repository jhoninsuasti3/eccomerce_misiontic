from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from marketApp.models.compra import Compra
from marketApp.serializers.compraSerializer import CompraSerializer
from marketApp.models.user import User
from marketApp.serializers.userSerializer import UserSerializer
from marketApp.models.detalle import Detalle
from marketApp.serializers.detalleSerializer import DetalleSerializer

class DetalleCreateView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = DetalleSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        print("----------------------------------------------------")
        serializer = DetalleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(serializer)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED
            )