from django.urls import path

from .views import (
    ClienteAPIView,
    ProductoAPIView,
    ProductoDetalleAPIView,
    PedidoAPIView,
    EventosUsuarioAPIView,
    RegistrarEventoAPIView,
    RegistroUsuarioAPIView,
    PerfilUsuarioAPIView
)

urlpatterns = [
    path('register/', RegistroUsuarioAPIView.as_view(), name='register'),
    path('perfil/', PerfilUsuarioAPIView.as_view(), name='perfil'),

    path('clientes/', ClienteAPIView.as_view(), name='clientes'),
    path('productos/', ProductoAPIView.as_view(), name='productos'),

    path('productos/<int:producto_id>/', ProductoDetalleAPIView.as_view(), name='producto_detalle'),

    path('pedidos/', PedidoAPIView.as_view(), name='pedidos'),

    path('eventos/', RegistrarEventoAPIView.as_view(), name='registrar_evento'),
    path('eventos/<str:user_id>/', EventosUsuarioAPIView.as_view(), name='eventos_usuario'),
]