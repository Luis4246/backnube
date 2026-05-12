import boto3

from datetime import datetime

from django.db import transaction

from .models import (
    Cliente,
    Pedido,
    DetallePedido
)


def registrar_evento(
    user_id,
    evento,
    descripcion,
    ip='127.0.0.1'
):

    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-east-1'
    )

    tabla = dynamodb.Table(
        'EventosUsuarios'
    )

    tabla.put_item(
        Item={

            'userId': str(user_id),

            'timestamp': datetime.now().isoformat(),

            'evento': evento,

            'descripcion': descripcion,

            'ip': ip
        }
    )


@transaction.atomic
def crear_pedido_con_detalles(
    data,
    ip='127.0.0.1'
):

    cliente = Cliente.objects.get(
        id=data['cliente']
    )

    pedido = Pedido.objects.create(
        cliente=cliente
    )

    detalles = data.get(
        'detalles',
        []
    )

    for item in detalles:

        DetallePedido.objects.create(

            pedido=pedido,

            producto=item['producto'],

            cantidad=item['cantidad'],

            precio_unitario=item['precio_unitario']
        )

    registrar_evento(

        user_id=cliente.id,

        evento='CREAR_PEDIDO',

        descripcion=f'Pedido {pedido.id} creado correctamente',

        ip=ip
    )

    return pedido