from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_attempt, name="register_attempt"),
    path('token/', views.token_send, name="token_send"),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('password-reset/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
]
