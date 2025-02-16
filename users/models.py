from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado a partir de AbstractUser.

    Basado en el modelo de usuario de Django y personalizado
    para añadir campos personalizados y autenticar a partir 
    del correo electrónico a diferencia del nombre de usuario
    utilizado por defecto.
    """
    username = None
    first_name = None
    last_name = None
    name = models.CharField(
        'Nombre',
        max_length=75
        )
    email = models.EmailField(
        'Correo',
        unique=True
        )
    is_business = models.BooleanField(
        'Es empresa',
        default=False
        )
    document = models.CharField(
        'Documento',
        max_length=15,
        blank=False,
        null=True,
        unique=True
        )
    contact_number = models.CharField(
        'Número de contacto',
        max_length=16,
        blank=False,
        null=True
        )
    address = models.CharField(
        'Dirección',
        max_length=255,
        blank=False,
        null=True
        )
    description = models.CharField(
        'Descripción',
        max_length=255,
        blank=True,
        null=True
        )
    is_staff = models.BooleanField(
        verbose_name="Es empleado",
        default=False
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
