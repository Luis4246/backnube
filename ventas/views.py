from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from .models import (
    Pedido,
    Cliente
)

from .serializers import (
    PedidoSerializer,
    ClienteSerializer
)

from .services import (
    crear_pedido_con_detalles
)


class ClienteAPIView(APIView):

    def get(self, request):

        clientes = Cliente.objects.all()

        serializer = ClienteSerializer(
            clientes,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ClienteSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PedidoAPIView(APIView):

    def get(self, request):

        pedidos = Pedido.objects.all()

        serializer = PedidoSerializer(
            pedidos,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        try:

            pedido = crear_pedido_con_detalles(

                request.data,

                ip=request.META.get(
                    'REMOTE_ADDR'
                )
            )

            serializer = PedidoSerializer(
                pedido
            )

            return Response(

                serializer.data,

                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {
                    'error': str(e)
                },

                status=status.HTTP_400_BAD_REQUEST
            )