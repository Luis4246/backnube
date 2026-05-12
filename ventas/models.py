from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )

    fecha = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nombre}'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.CharField(max_length=150)
    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.producto} x {self.cantidad}'