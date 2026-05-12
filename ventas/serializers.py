from rest_framework import serializers
from .models import Cliente, Pedido, DetallePedido


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
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(
        source='cliente.nombre',
        read_only=True
    )

    class Meta:
        model = Pedido
        fields = [
            'id',
            'cliente',
            'cliente_nombre',
            'fecha',
            'total',
            'detalles'
        ]


class CrearDetallePedidoSerializer(serializers.Serializer):
    producto = serializers.CharField(max_length=150)
    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )


class CrearPedidoSerializer(serializers.Serializer):
    cliente = serializers.IntegerField()
    detalles = CrearDetallePedidoSerializer(many=True)

    def validate_detalles(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(
                'Debe agregar al menos un producto al pedido.'
            )
        return value