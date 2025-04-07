from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import \
    UnicodeUsernameValidator

from clients.models import Client
from clients.validators import (
    StrongPasswordValidator, 
    AllowedEmailValidator,
)


class ClientAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), required=False
    )

    class Meta:
        model = Client
        fields = "__all__"

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:  # Проверяем, если пароль вообще был изменен
            validator = StrongPasswordValidator()
            try:
                validator(value=password)
            except ValidationError as e:
                raise ValidationError(e.messages)  # Выдаем ошибку в админке
            return make_password(password)
        return password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            validator = UnicodeUsernameValidator()
            try:
                validator(username)
            except ValidationError as e:
                raise ValidationError(e.messages)  # Ошибка в админке
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            validator = AllowedEmailValidator()
            try:
                validator(email)
            except ValidationError as e:
                raise ValidationError(e.messages)  # Ошибка в админке
        return email
    