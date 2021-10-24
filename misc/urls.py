from django.urls import path
from .views import *

app_name = "misc"

urlpatterns = [path('about', about_page, name='about-page')]
