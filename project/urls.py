from django.http import HttpResponseNotFound
from django.urls import path, include
from . import views

urlpatterns = [
    path('default_dashboard/', views.default_dashboard, name="default_dashboard"),
    path('tech_dashboard', views.tech_dashboard, name="tech_dashboard"),
    path('finance_dashboard', views.finance_dashboard, name="finance_dashboard"),
    path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),
    path('add_record', views.add_record, name='add_record'),
    path('booking_record/<int:pk>', views.booking_record, name='booking_record'),
    path('records', views.record, name='records'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name='logout'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('status/', views.status, name='status'),
    path('customer/', views.customer, name='customer'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('customer_record/<int:pk>', views.customer_record, name='customer_record'),
    path('delete_customer/<int:pk>', views.delete_customer, name='delete_customer'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('update_customer/<int:pk>', views.update_customer, name='update_customer'),
    path('favicon.ico', lambda request: HttpResponseNotFound()),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('test/', views.test, name="test")

    


]
