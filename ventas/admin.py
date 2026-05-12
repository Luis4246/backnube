from django.contrib import admin

from .models import (
    Cliente,
    Pedido,
    DetallePedido
)

admin.site.register(Cliente)

admin.site.register(Pedido)

admin.site.register(DetallePedido)