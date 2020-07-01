from django.urls import path
from .views import *

urlpatterns = [
    path('', redirect_page, name='redirect_page'),
    path('bank/', bank, name='bank'),
    path('footanddrink/', footanddrink, name='footanddrink'),
]
