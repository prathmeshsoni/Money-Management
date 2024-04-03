from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.admin_private),
    path('logout/', views.logout_private_admin),
    path('view/', views.admin_private_view, {'template_name': 'transaction.html'}),
    path('viewe/', views.category_add),
    path('get_data/', views.get_date_transaction),
    path('updatepra/', views.get_value),
    path('remove_transaction/', views.remove_transaction),
    path('balance/', views.check_balance),
    path('view/<str:other>/', views.view_all),
    path('view/type/<str:hid>/', views.view_type),
    path('view/account/<str:hid>/', views.view_account),
    path('view/category/<str:hid>/', views.view_category),
    path('search/', views.search_page),
    path('chart/<str:hid>/', views.chart_page),
    path('chart/', views.chart_page_1),
]
