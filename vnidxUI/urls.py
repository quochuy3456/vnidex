from django.urls import path
from .views import *

urlpatterns = [
    path('bank', bank, name='bank'),
    path('travel', travel, name='travel'),
]
