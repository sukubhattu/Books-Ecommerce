from django.contrib import admin
from django.db import models
from .models import Book, Review


@admin.action(description='Mark selected as paid')
def update_to_paid(modeladmin, request, queryset):
    queryset.update(is_paid=True)


class ReviewInline(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = (
        'name',
        'author',
        'price',
        'seller_paypal_email',
        'amount_to_be_paid',
        'category',
        'is_sold',
        'is_paid',
    )
    list_filter = ['category', 'is_paid', 'is_sold']
    search_fields = ['id', 'name', 'author']
    actions = [update_to_paid]


admin.site.register(Book, BookAdmin)
admin.site.register(Review)
