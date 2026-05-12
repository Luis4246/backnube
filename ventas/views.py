import boto3
from boto3.dynamodb.conditions import Key

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cliente, Pedido
from .serializers import (
    ClienteSerializer,
    PedidoSerializer,
    CrearPedidoSerializer
)
from .services import crear_pedido_con_detalles, registrar_evento


class ClienteAPIView(APIView):

    def get(self, request):
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)

        registrar_evento(
            user_id='sistema',
            evento='CONSULTAR_CLIENTES',
            descripcion='Se consultó el listado de clientes'
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ClienteSerializer(data=request.data)

        if serializer.is_valid():
            cliente = serializer.save()

            registrar_evento(
                user_id=cliente.id,
                evento='CREAR_CLIENTE',
                descripcion=f'Se creó el cliente {cliente.nombre}',
                metadata={
                    'cliente_id': cliente.id,
                    'email': cliente.email
                }
            )

            return Response(
                ClienteSerializer(cliente).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PedidoAPIView(APIView):

    def get(self, request):
        pedidos = Pedido.objects.all().order_by('-fecha')
        serializer = PedidoSerializer(pedidos, many=True)

        registrar_evento(
            user_id='sistema',
            evento='CONSULTAR_PEDIDOS',
            descripcion='Se consultó el listado de pedidos'
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CrearPedidoSerializer(data=request.data)

        if serializer.is_valid():
            try:
                pedido = crear_pedido_con_detalles(
                    cliente_id=serializer.validated_data['cliente'],
                    detalles=serializer.validated_data['detalles']
                )

                return Response(
                    PedidoSerializer(pedido).data,
                    status=status.HTTP_201_CREATED
                )

            except Cliente.DoesNotExist:
                return Response(
                    {'error': 'El cliente no existe.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class EventosUsuarioAPIView(APIView):

    def get(self, request, user_id):
        try:
            dynamodb = boto3.resource(
                'dynamodb',
                region_name='us-east-1'
            )

            tabla = dynamodb.Table('EventosUsuarios')

            response = tabla.query(
                KeyConditionExpression=Key('userId').eq(str(user_id)),
                ScanIndexForward=False
            )

            return Response(response.get('Items', []))

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RegistrarEventoAPIView(APIView):

    def post(self, request):
        user_id = request.data.get('userId')
        evento = request.data.get('evento')
        descripcion = request.data.get('descripcion', '')
        metadata = request.data.get('metadata', {})

        if not user_id or not evento:
            return Response(
                {'error': 'userId y evento son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = registrar_evento(
                user_id=user_id,
                evento=evento,
                descripcion=descripcion,
                metadata=metadata
            )

            return Response(
                {
                    'mensaje': 'Evento registrado correctamente.',
                    'evento': item
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )