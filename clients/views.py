import logging
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages

from clients.models import Client

logger = logging.getLogger()


class BasePageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(content="Hello")


class RegistrationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="reg.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        email = request.POST.get("email")
        raw_password = request.POST.get("password")

        if len(raw_password) < 8:
            messages.error(request, message="малый пароль")
            return render(request=request, template_name="reg.html")

        try:
            Client.objects.create(
                email=email,
                username=username,
                password=make_password(raw_password)
            )
            messages.info(request, message="спасибо за регулю")
            return render(request=request, template_name="reg.html")

        except Exception as e:
            logger.error("Ошибка при регистрации", exc_info=e)
            messages.error(request, message=str(e))
            return render(request=request, template_name="reg.html")


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")
        client: Client | None = authenticate(
            request=request,
            username=username,
            password=password
        )

        if not client:
            messages.error(request=request, message="Неверный логин или пароль!")
            return render(request, "login.html")

        login(request=request, user=client)
        messages.success(request, "Вы успешно вошли!")
        return redirect("home")



