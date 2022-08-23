from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from marketApp.models.producto import Producto
from marketApp.serializers.productoSerializer import ProductoSerializer

class ProductoCreateView(generics.RetrieveAPIView):
    serializer_class = ProductoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized token'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductoSerializer.crear(self, request, user=valid_data['user_id'])
        stringResponse = None

        if serializer == None:
            stringStatus = status.HTTP_401_UNAUTHORIZED
            stringResponse = {'detail':'Unauthorized Request'}
        else:
            serializer.save()
            stringStatus = status.HTTP_201_CREATED
            stringResponse = None

        return Response(
            stringResponse,
            status=stringStatus
            )
    
    def get(self, request, *args, **kwargs):
    
        stringStatus = status.HTTP_200_OK
        stringResponse = ProductoSerializer.crearRespuesta(producto = kwargs['pk'])
            
        return Response(
            stringResponse,
            status=stringStatus
            )

    def put(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        stringStatus = status.HTTP_202_ACCEPTED
        stringRespuesta = ProductoSerializer.actualizar(request, clave = valid_data['user_id'], producto = kwargs['pk'])

        if stringRespuesta == None:
            stringStatus = status.HTTP_401_UNAUTHORIZED
            respuesta = {'detail':'Unauthorized Request'}
        else:
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
        stringRespuesta = ProductoSerializer.eliminar(clave = valid_data['user_id'], producto = kwargs['pk'])

        if stringRespuesta == None:
            stringStatus = status.HTTP_401_UNAUTHORIZED
            respuesta = {'detail':'Unauthorized Request'}
        else:
            respuesta = None

        return Response(
            respuesta,
            status=stringStatus
            )