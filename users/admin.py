from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()

from .models import UserPurchase, UserPurchaseSession, CustomUser


class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
        )


class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    prepopulated_fields = {
        'username': (
            'first_name',
            'last_name',
        )
    }

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'first_name',
                    'last_name',
                    'username',
                    'email',
                    'password1',
                    'password2',
                ),
            },
        ),
    )


class UserPurchaseAdmin(admin.ModelAdmin):
    search_fields = [
        'book__name',
        'buyer__email',
        'seller__email',
        'buyer__first_name',
        'seller__first_name',
        'buyer__last_name',
        'buyer__last_name',
    ]
    list_display = ['id', 'buyer', 'seller', 'book', 'book_price']


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Paypal Email Address',
            {
                'fields': ('paypal_email_address',),
            },
        ),
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'email', 'username', 'paypal_email_address']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserPurchase, UserPurchaseAdmin)
admin.site.register(UserPurchaseSession)
