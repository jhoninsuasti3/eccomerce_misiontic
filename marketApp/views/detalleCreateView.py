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
    queryset = Detalle.objects.all()
    serializer_class = DetalleSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = DetalleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stringRespuesta = serializer.save()

        return Response(
            DetalleSerializer.respuesta(stringRespuesta),
            status=status.HTTP_201_CREATED
            )
    
    def get(self, request, *args, **kwargs):
    
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        stringStatus = status.HTTP_200_OK
        stringResponse = DetalleSerializer.crearRespuesta(clave = valid_data['user_id'], detalle = kwargs['pk'])
        print(stringResponse)

        for key in stringResponse:
            if key == 'detail' :
                stringStatus = status.HTTP_401_UNAUTHORIZED
            
        return Response(
            stringResponse,
            status=stringStatus
            )

    def put(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        stringStatus = status.HTTP_202_ACCEPTED
        stringRespuesta = DetalleSerializer.actualizar(request, clave = valid_data['user_id'], detalle = kwargs['pk'])

        for key in stringRespuesta:
            if key == 'detail':
                stringStatus = status.HTTP_401_UNAUTHORIZED
                respuesta = stringRespuesta
            if key == 'estado':
                respuesta = None
        return Response(
            respuesta,
            status=stringStatus
            )

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        stringStatus = status.HTTP_202_ACCEPTED
        stringRespuesta = DetalleSerializer.eliminar(clave = valid_data['user_id'], detalle = kwargs['pk'])

        for key in stringRespuesta:
            if key == 'detail':
                stringStatus = status.HTTP_401_UNAUTHORIZED
                respuesta = stringRespuesta
            if key == 'estado':
                respuesta = None
        return Response(
            respuesta,
            status=stringStatus
            )