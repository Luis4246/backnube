from rest_framework import serializers
from .models import Cliente, Producto, Pedido, DetallePedido


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetallePedido
        fields = [
            'id',
            'producto',
            'producto_nombre',
            'cantidad',
            'precio_unitario',
            'subtotal'
        ]


class PedidoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_email = serializers.CharField(source='cliente.email', read_only=True)
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id',
            'cliente',
            'cliente_nombre',
            'cliente_email',
            'fecha',
            'total',
            'estado',
            'detalles'
        ]


class CrearDetallePedidoSerializer(serializers.Serializer):
    producto = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)


class CrearPedidoSerializer(serializers.Serializer):
    detalles = CrearDetallePedidoSerializer(many=True)