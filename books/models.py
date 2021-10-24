from django.contrib import auth
from django.db import models
from django.urls import reverse
from django.conf import settings


from .constants import BOOK_TYPES


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Book(BaseModel):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.FloatField()
    cover = models.ImageField(upload_to='covers/', blank=True)
    description = models.TextField()
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=45)
    category = models.CharField(max_length=20, choices=BOOK_TYPES)
    is_featured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:book-detail', args=[str(self.id)])

    @property
    def cover_URL(self):
        try:
            url = self.cover.url
        except:
            url = ''
        return url

    @property
    def amount_to_be_paid(self):
        return round(self.price * 0.95, 2)

    @property
    def seller_paypal_email(self):
        return self.seller.paypal_email_address


class Review(BaseModel):

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    review = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.review
