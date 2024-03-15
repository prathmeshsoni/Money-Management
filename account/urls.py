from django.urls import path

from . import views

urlpatterns = [
    path('', views.acc_page),
    path("updateCat/", views.updateacc),
    path('remove_cat/', views.remove_acc),
]
