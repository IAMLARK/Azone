from django.http import HttpResponseNotFound
from django.urls import path
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
    path('update_customer/<int:pk>', views.update_customer, name='update_customer'),
    path('favicon.ico', lambda request: HttpResponseNotFound()),
    


]
