from django.urls import path 
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('brand/add/', views.add_brand, name='add_brand'),
    path('brand/list/', views.brand_list, name='brand_list'),
    path('brand/edit/<int:id>/', views.edit_brand, name='edit_brand'),
    path('brand/delete/<int:id>/', views.delete_brand, name='delete_brand'),
    path('vehicle/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicle/list/', views.vehicle_list, name='vehicle_list'),
    path('vehicle/edit/<int:id>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicle/delete/<int:id>/', views.delete_vehicle, name='delete_vehicle'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/list/', views.product_list, name='product_list'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/super-admin/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('inventory/', views.inventory_dashboard, name='inventory_dashboard'),
    path('dashboard/sales/', views.sales_dashboard, name='sales_dashboard'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
