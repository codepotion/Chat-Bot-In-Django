from django.urls import path
from .views import *
app_name = 'landing'

urlpatterns = [
    path('', LandingFunction, name='LandingFunction'),
    path('chatting-requests/', ChattingRequest, name='ChattingRequest'),
]
