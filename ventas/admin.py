from django.urls import path
from .views import (
    ClienteAPIView,
    PedidoAPIView,
    EventosUsuarioAPIView,
    RegistrarEventoAPIView
)

urlpatterns = [
    path('clientes/', ClienteAPIView.as_view(), name='clientes'),
    path('pedidos/', PedidoAPIView.as_view(), name='pedidos'),
    path('eventos/<str:user_id>/', EventosUsuarioAPIView.as_view(), name='eventos_usuario'),
    path('eventos/', RegistrarEventoAPIView.as_view(), name='registrar_evento'),
]