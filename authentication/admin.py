from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # colonnes affichées dans la liste
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    # recherche
    search_fields = ("username", "email")

    # champs affichés dans le formulaire de détail
    fieldsets = UserAdmin.fieldsets + (
        ("Infos supplémentaires", {"fields": ("profile_photo", "role")}),
    )

    # champs disponibles lors de la création d'un user dans l'admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Infos supplémentaires", {"fields": ("profile_photo", "role")}),
    )