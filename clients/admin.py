# from django.contrib import admin
# from clients.models import Client

# class ClientAdmin(admin.ModelAdmin):
#     model = Client
#     list_display = ("email", "username", "date_created", "is_superuser")
#     search_fields = ("email", 'username')
#     list_filter = ("date_created", "gender")  # Исправлено на date_created
#     list_per_page = 50

# admin.site.register(Client, ClientAdmin)


from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm

from clients.models import Client
from clients.forms import ClientAdminForm


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    change_password_form = AdminPasswordChangeForm
    model = Client
    list_display = (
        "email", "username", "first_name", "last_name", 
        "is_superuser", "date_created", "last_login",
    )
    list_filter = (
        "email", "username", "date_created", "last_login",
    )
    search_fields = (
        "email", "username", "date_created", "last_login",
    )