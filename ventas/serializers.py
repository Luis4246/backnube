from rest_framework import serializers

from .models import (
    Cliente,
    Pedido,
    DetallePedido
)


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'


class DetallePedidoSerializer(serializers.ModelSerializer):

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = DetallePedido

        fields = [
            'id',
            'producto',
            'cantidad',
            'precio_unitario',
            'subtotal'
        ]

    def get_subtotal(self, obj):

        return obj.subtotal()


class PedidoSerializer(serializers.ModelSerializer):

    detalles = DetallePedidoSerializer(
        many=True
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido

        fields = [
            'id',
            'fecha',
            'estado',
            'cliente',
            'detalles',
            'total'
        ]

    def get_total(self, obj):

        return obj.total()