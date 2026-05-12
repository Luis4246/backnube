from django.urls import path

from .views import (
    ClienteAPIView,
    PedidoAPIView
)

urlpatterns = [

    path(
        'clientes/',
        ClienteAPIView.as_view(),
        name='clientes'
    ),

    path(
        'pedidos/',
        PedidoAPIView.as_view(),
        name='pedidos'
    ),
]