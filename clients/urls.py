from django.urls import path

from clients.views import HomeView, AuthView, RegistrationView


urlpatterns = [
    path(route="admin/", view=HomeView.as_view(), name="admin"),
    path(route="login/", view=AuthView.as_view(), name="login"),
    path(route="reg/", view=RegistrationView.as_view(), name="reg"),
]
