from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Perfil(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES, default='empleado')

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

class Producto(models.Model):
    TIPO_CHOICES = (
        ('medicamento', 'Medicamento'),
        ('aseo', 'Producto de Aseo'),
        ('cosmetico', 'Cosmético'),
        ('otros', 'Otros'),
    )
    FORMA_CHOICES = (
        ('capsula', 'Cápsula'),
        ('tableta', 'Tableta'),
        ('unguento', 'Ungüento'),
        ('crema_topica', 'Crema tópica'),
        ('vaginal', 'Vaginal'),
        ('solucion', 'Solución'),
        ('otros', 'Otros'),
    )

    # Campos básicos existentes
    nombre = models.CharField(max_length=200)
    principio_activo = models.CharField(max_length=200, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    fecha_vencimiento = models.DateField()
    requiere_receta = models.BooleanField(default=False)

    # Nuevos campos
    tipo_producto = models.CharField(max_length=20, choices=TIPO_CHOICES, default='medicamento')
    forma_farmaceutica = models.CharField(max_length=20, choices=FORMA_CHOICES, blank=True, null=True, help_text="Si es medicamento")

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"

    def esta_proximo_a_vencer(self, dias=30):
        hoy = timezone.now().date()
        return self.fecha_vencimiento <= hoy + timedelta(days=dias)

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Venta de {self.producto.nombre} - {self.fecha.strftime('%d/%m/%Y')}"