from django.urls import path
from .views import user_profile, user_purchase_view

app_name = 'users'
urlpatterns = [
    path('profile/', user_profile, name="profile"),
    # path('<int:id>/book-purchase/', user_purchase_view, name="purchase"),
]
