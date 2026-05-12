import boto3
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.core.mail import send_mail

from .models import Cliente, Producto, Pedido, DetallePedido


def registrar_evento(user_id, evento, descripcion='', metadata=None):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-east-1'
    )

    tabla = dynamodb.Table('EventosUsuario')

    timestamp = datetime.utcnow().isoformat()

    item = {
        'userId': str(user_id),
        'Timestamp': timestamp,
        'evento': evento,
        'descripcion': descripcion,
        'metadata': metadata or {}
    }

    tabla.put_item(Item=item)

    return item


def enviar_correo_confirmacion_pedido(pedido):
    asunto = f'Confirmación de pedido #{pedido.id}'

    mensaje = f"""
Hola {pedido.cliente.nombre},

Tu pedido fue registrado correctamente.

Número de pedido: {pedido.id}
Estado: {pedido.estado}
Total: {pedido.total}

Detalle del pedido:
"""

    for detalle in pedido.detalles.all():
        mensaje += (
            f"\n- {detalle.producto.nombre} "
            f"x {detalle.cantidad} "
            f"= {detalle.subtotal}"
        )

    mensaje += "\n\nGracias por tu compra."

    send_mail(
        asunto,
        mensaje,
        None,
        [pedido.cliente.email],
        fail_silently=False
    )


@transaction.atomic
def crear_pedido_con_detalles(user, detalles):
    if not user.email:
        raise Exception('El usuario no tiene correo registrado.')

    cliente, creado = Cliente.objects.get_or_create(
        email=user.email,
        defaults={
            'nombre': user.username
        }
    )

    pedido = Pedido.objects.create(
        cliente=cliente,
        total=Decimal('0.00'),
        estado='pendiente'
    )

    total = Decimal('0.00')

    for detalle in detalles:
        producto_id = detalle['producto']
        cantidad = detalle['cantidad']

        producto = Producto.objects.get(id=producto_id)

        if producto.stock < cantidad:
            raise Exception(
                f'No hay stock suficiente para el producto {producto.nombre}.'
            )

        precio_unitario = producto.precio
        subtotal = precio_unitario * cantidad
        total += subtotal

        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )

        producto.stock -= cantidad
        producto.save()

    pedido.total = total
    pedido.save()

    registrar_evento(
        user_id=user.id,
        evento='CREAR_PEDIDO',
        descripcion=f'El usuario {user.username} creó el pedido #{pedido.id}',
        metadata={
            'pedido_id': pedido.id,
            'cliente_id': cliente.id,
            'cliente_email': cliente.email,
            'total': str(pedido.total),
            'cantidad_productos': len(detalles)
        }
    )

    enviar_correo_confirmacion_pedido(pedido)

    return pedido