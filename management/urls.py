from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_private),
    path('ss/', views.dd),
    path('view/', views.admin_private_view),
    path('viewe/', views.viewes),
    path('view/<str:hid>/', views.view_all),
    path('balance/', views.check_balance),
    # path('view/<int:hid>',views.private_view),
    path('logout/', views.logout_private_admin),
    path('updatepra/',views.updatepra),
    path('remove_pri/<int:hid>',views.remove_pri),
    path('view/type/<str:hid>/',views.view_type),
    path('view/account/<str:hid>/',views.view_account),
    path('view/category/<str:hid>/',views.view_category),
    # path('remove_photo/<int:hid>',views.remove_photo),
    # path('download_data/', views.download_data),
]