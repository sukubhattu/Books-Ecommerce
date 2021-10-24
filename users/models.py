from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from books.models import Book


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    paypal_email_address = models.EmailField(blank=True, null=True)


class UserPurchase(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer')
    address_line1 = models.CharField(max_length=300, blank=True, null=True)
    address_line2 = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300)
    shipping_address_name = models.CharField(max_length=300, blank=True, null=True)
    zipcode = models.IntegerField()
    is_complete = models.BooleanField(default=False)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.id)

    @property
    def book_price(self):
        return self.book.price


class UserPurchaseSession(models.Model):
    session_id = models.TextField()
