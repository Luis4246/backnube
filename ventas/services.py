import boto3
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from .models import Cliente, Pedido, DetallePedido


def registrar_evento(user_id, evento, descripcion='', metadata=None):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-east-1'
    )

    tabla = dynamodb.Table('EventosUsuarios')

    timestamp = datetime.utcnow().isoformat()

    item = {
        'userId': str(user_id),
        'timestamp': timestamp,
        'evento': evento,
        'descripcion': descripcion,
        'metadata': metadata or {}
    }

    tabla.put_item(Item=item)

    return item


@transaction.atomic
def crear_pedido_con_detalles(cliente_id, detalles):
    cliente = Cliente.objects.get(id=cliente_id)

    pedido = Pedido.objects.create(
        cliente=cliente,
        total=0
    )

    total = Decimal('0.00')

    for detalle in detalles:
        cantidad = detalle['cantidad']
        precio_unitario = detalle['precio_unitario']

        subtotal = cantidad * precio_unitario
        total += subtotal

        DetallePedido.objects.create(
            pedido=pedido,
            producto=detalle['producto'],
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )

    pedido.total = total
    pedido.save()

    registrar_evento(
        user_id=cliente.id,
        evento='CREAR_PEDIDO',
        descripcion=f'El cliente {cliente.nombre} creó el pedido #{pedido.id}',
        metadata={
            'pedido_id': pedido.id,
            'total': str(pedido.total),
            'cantidad_productos': len(detalles)
        }
    )

    return pedido