from rest_framework.decorators import (
    api_view
)

from rest_framework.response import (
    Response
)

from .models import Pedido

from .serializers import (
    PedidoSerializer
)


@api_view(['GET'])
def historial_pedidos(request):

    pedidos = Pedido.objects.all()

    serializer = PedidoSerializer(
        pedidos,
        many=True
    )

    return Response(serializer.data)