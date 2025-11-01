from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# специальный класс для отображения CustomUser в админке
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'uuid')
    list_filter = ('is_staff', )
    ordering = ('email',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'token', 'date_joined', 'is_verified', 'timezone')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff')}
        ),
    )
