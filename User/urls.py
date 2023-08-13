from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.register_attempt, name="register_attempt"),
    path('send_email/', views.send_email_, name="register_attempt"),
    path('password-reset/', views.forget_password),

    path('register/', views.register_attempt, name="register_attempt"),
    path('token/', views.token_send, name="token_send"),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('password-reset-confirm/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url='/',
         ),
         name='password_reset_confirmm'
     ),
]
