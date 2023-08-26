from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import Customer, EmailRegisterData, Profile, Token, User


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'phone', 'city')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'full_name', 'is_staff')
    search_fields = ('username', 'full_name')
    ordering = ('id',)


admin.site.register(User, CustomUserAdmin)


@admin.register(Token)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created')
    readonly_fields = ('full_name', 'project_name',
                       'phone_number', 'category_id', 'address',)
    list_filter = ('created',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number')

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


