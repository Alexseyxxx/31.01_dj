from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
    Group,
    Permission
)

class ClientManager(BaseUserManager):
    def create_superuser(
            self,
            username:str,
            email:str,
            password:str,
    ) -> "Client":
       """Creste super user."""
       client: Client=Client()
       client.email=self.normalize_email(email=email)
       client.username=username
       client.set_password(raw_password=password)
       client.is_active=True
       client.is_staff=True
       client.is_superuser=True
       client.save()
       return client
class Client(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="никнейм",
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="эл. почта",
        max_length=100,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        verbose_name="активный",
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name="сотрудник",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="администратор",
        default=False,
    )
    gender = models.CharField(
        verbose_name="пол",
        max_length=10,  
        blank=True, 
        null=True, 
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )
    last_login = models.DateTimeField(
        verbose_name="последняя дата входа",
        blank=True, 
        null=True,
    )

  
    groups = models.ManyToManyField(
        to=Group,
        related_name="clients_groups", 
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="clients_permissions",  
    )


    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects =ClientManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self) -> str:
        return f"{self.username} | {self.email} | {self.date_created}"
