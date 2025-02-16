from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "is_business")
    list_filter = ("email", "is_business", "is_staff", "is_active",)
    fieldsets = (
        ("Información personal", {
            "fields": (
                "name",
                "is_business",
                "document",
                "contact_number",
                "address",
                "description",
                )}),
        ("Información de acceso", {
            "fields": (
                "email",
                "password",
                )}),
        ("Permisos", {
            "fields": (
                "is_staff",
                "is_active",
                "groups",
                "user_permissions"
                )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    list_per_page = 20

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
