from django.urls import path

from . import views

urlpatterns = [
    path('', views.type_page),
    path('updateCat/', views.updatetype),
    path('remove_cat/', views.remove_type),
]
