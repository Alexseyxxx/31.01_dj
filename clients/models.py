import logging
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
    Group,
    Permission,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

from clients.validators import StrongPasswordValidator, AllowedEmailValidator


logger = logging.getLogger(name=__name__)

class ClientManager(BaseUserManager):
    """Manager for Clients."""

    def validate(self, **kwargs) -> None:
        required_fields = ["username", "email", "password"]
        
        for field in required_fields:
            if not kwargs.get(field):
                raise ValidationError(f"{field.capitalize()} is required.")
        
        # Проверяем username через встроенный валидатор Django
        username_validator = UnicodeUsernameValidator()
        username_validator(kwargs["username"])

        # Проверяем пароль через наш кастомный валидатор
        password_validator = StrongPasswordValidator()
        password_validator(kwargs["password"])

        # Проверяем email через наш валидатор
        email_validator = AllowedEmailValidator()
        email_validator(kwargs["email"])

        logger.debug("All validations passed for %s", kwargs["username"])
    
    def create_superuser(self, username: str, email: str, password: str) -> "Client":
        """Create super user."""
        self.validate(username=username, email=email, password=password)
        
        client = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        client.set_password(password)
        client.is_active = True
        client.is_staff = True
        client.is_superuser = True
        client.save(using=self._db)
        return client


class Client(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="никнейм",
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
    )
    birthday = models.DateField(
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="эл. почта",
        max_length=100,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group, blank=True, related_name="clients_group")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="clients_permissions")

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"
    objects = ClientManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f"{self.username} | {self.email} | {self.date_created}"



