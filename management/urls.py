from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_private),
    path('logout/', views.logout_private_admin),
    path('view/', views.admin_private_view, {'template_name': 'private_des.html'}),
    path('view1/', views.admin_private_view, {'template_name': 'private-s.html'}),
    path('get_data/', views.get_date_transaction),
    path('search/', views.search_page),
    path('chart/<str:hid>/', views.chart_page),
    path('chart/', views.chart_page_1),
    path('viewe/', views.category_add),
    path('view/<str:other>', views.view_all),
    path('balance/', views.check_balance),
    path('updatepra/', views.get_value),
    path('remove_pri/', views.remove_pri),
    path('view/type/<str:hid>/', views.view_type),
    path('view/account/<str:hid>/', views.view_account),
    path('view/category/<str:hid>/', views.view_category),
    path('user-log/', views.user_log),
    path('change-password/', views.custom_change_password, name='change_password')
    # path('remove_photo/<int:hid>',views.remove_photo),
    # path('download_data/', views.download_data),
]
