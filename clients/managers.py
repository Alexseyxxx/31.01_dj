# clients/managers.py
from django.contrib.auth.models import BaseUserManager
from clients.validators import StrongPasswordValidator, AllowedEmailValidator
from django.core.exceptions import ValidationError

class ClientManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        if not username:
            raise ValueError("Username обязателен")

        # Валидация
        AllowedEmailValidator()(email)
        StrongPasswordValidator().validate(password)

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        # Валидация
        AllowedEmailValidator()(email)
        StrongPasswordValidator().validate(password)

        return self.create_user(username, email, password, **extra_fields)
