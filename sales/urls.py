from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
    path('table/', views.sales_table, name='table'),
    path('manage/', views.manage_sales, name='manage'),
    path('add/', views.add_sale, name='add'),
    path('edit/<int:pk>/', views.edit_sale, name='edit'),
    path('delete/<int:pk>/', views.delete_sale, name='delete'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
