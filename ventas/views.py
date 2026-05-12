import boto3
from boto3.dynamodb.conditions import Key

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Cliente, Pedido
from .serializers import (
    ClienteSerializer,
    PedidoSerializer,
    CrearPedidoSerializer
)
from .services import crear_pedido_con_detalles, registrar_evento


class RegistroUsuarioAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        rol = request.data.get('rol', 'cliente')

        if not username or not password:
            return Response(
                {'error': 'username y password son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'El usuario ya existe.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        if rol == 'operador':
            user.is_staff = True
            user.save()

        return Response(
            {
                'mensaje': 'Usuario creado correctamente.',
                'usuario': user.username,
                'email': user.email,
                'rol': 'operador' if user.is_staff else 'cliente'
            },
            status=status.HTTP_201_CREATED
        )


class PerfilUsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'rol': 'operador' if user.is_staff else 'cliente'
        })


class ClienteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClienteSerializer(data=request.data)

        if serializer.is_valid():
            cliente = serializer.save()

            registrar_evento(
                user_id=request.user.id,
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_staff:
            pedidos = Pedido.objects.all().order_by('-fecha')
        else:
            pedidos = Pedido.objects.filter(cliente__email=user.email).order_by('-fecha')

        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CrearPedidoSerializer(data=request.data)

        if serializer.is_valid():
            try:
                cliente_id = serializer.validated_data['cliente']

                if not request.user.is_staff:
                    cliente = Cliente.objects.get(id=cliente_id)

                    if cliente.email != request.user.email:
                        return Response(
                            {'error': 'No puedes crear pedidos para otro cliente.'},
                            status=status.HTTP_403_FORBIDDEN
                        )

                pedido = crear_pedido_con_detalles(
                    cliente_id=cliente_id,
                    detalles=serializer.validated_data['detalles']
                )

                registrar_evento(
                    user_id=request.user.id,
                    evento='CREAR_PEDIDO',
                    descripcion=f'Se creó el pedido {pedido.id}',
                    metadata={
                        'pedido_id': pedido.id
                    }
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventosUsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            if not request.user.is_staff and str(request.user.id) != str(user_id):
                return Response(
                    {'error': 'No tienes permiso para ver estos eventos.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            dynamodb = boto3.resource(
                'dynamodb',
                region_name='us-east-1'
            )

            tabla = dynamodb.Table('EventosUsuario')

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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('userId', request.user.id)
        evento = request.data.get('evento')
        descripcion = request.data.get('descripcion', '')
        metadata = request.data.get('metadata', {})

        if not request.user.is_staff and str(user_id) != str(request.user.id):
            return Response(
                {'error': 'No puedes registrar eventos para otro usuario.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not evento:
            return Response(
                {'error': 'evento es obligatorio.'},
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