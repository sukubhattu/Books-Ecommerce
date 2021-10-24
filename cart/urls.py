from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('update_item/', update_item, name='update-item'),
    path('get_cart_count', get_cart_count, name='get_cart_count'),
    path('checkout_stripe', checkout_stripe, name='checkout_stripe'),
    path('stripe_checkout_session', stripe_checkout_session, name='stripe_checkout_session'),
    path('success/', success),
    path('cancelled/', cancelled),
    path('stripe_payout_session', stripe_payout_session),
]
