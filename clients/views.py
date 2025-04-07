from django.views import View
from django.contrib.auth import aauthenticate, alogin
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages

from clients.models import Client
from clients.validators import StrongPasswordValidator


class HomeView(View):
    """Home View."""

    async def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(content="Hello")


class AuthView(View):
    """Auth view."""

    async def get(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponse:
        return render(request=request, template_name="login.html")

    async def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")
        client: Client = await aauthenticate(
            request=request, username=username, password=password
        )
        if client:
            await alogin(request=request, user=client)
            return redirect(to="home")
        else:
            messages.error(
                request=request, message="Неверный логин или пароль!"
            )
        return render(request=request, template_name="login.html")
        

class RegistrationView(View):
    """Registration View."""

    async def get(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponse:
        return render(request=request, template_name="reg.html")
    
    async def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponse:
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            StrongPasswordValidator()(value=password)
        except ValidationError as e:
            messages.error(request=request, message=str(e))
            return render(request, "reg.html")

        try:
            _, created = await Client.objects.aget_or_create(
                username=username, email=email, 
                defaults={
                    "password": make_password(password=password)
                },
            )
        except ValidationError as e:
            messages.error(request=request, message=str(e))
            return render(request, "reg.html")
        
        if not created:
            messages.error(
                request=request, 
                message="Такой пользователь уже существует!"
            )
            return render(request, "reg.html")

        messages.success(request, "Вы успешно зарегистрированы!")
        return redirect("home")
