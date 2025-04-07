"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# settings/urls.py

# from django.contrib import admin
# from django.urls import path, include
# from django.conf.urls.static import static
# from django.conf import settings
# from clients.views import RegistrationView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("reg/", RegistrationView.as_view(), name="reg"),  # теперь /reg/ работает напрямую
#     path("clients/", include("clients.urls")),
    
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
#     + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += [
#         path('__debug__/', include('debug_toolbar.urls')),
#     ]


from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from clients.views import HomeView, AuthView, RegistrationView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),  # 👈 Корень сайта
    path('admin/', admin.site.urls),
    path("reg/", RegistrationView.as_view(), name="reg"),
    path("login/", AuthView.as_view(), name="login"),
    path("clients/", include("clients.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
