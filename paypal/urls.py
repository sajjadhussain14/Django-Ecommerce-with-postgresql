 
from django.contrib import admin
from django.urls import path

from . import views
app_name="paypal"
urlpatterns = [
    path('', views.index, name="index"),
    path('checkout/', views.paypal_checkout, name='paypal_checkout'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('cancel_payment/', views.cancel_payment, name='cancel_payment'),
    path('thank-you/', views.thank_you, name='thank_you'),

]
