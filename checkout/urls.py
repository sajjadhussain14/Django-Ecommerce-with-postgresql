from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "checkout"

from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("guest-checkout/", views.guest_chekout_Create_account, name="guest_chekout_Create_account"),
    
    path("returning-customer/", views.returning_customer, name="returning_customer"),
    
    path("update-billing/", views.update_billing, name="update_billing"),
    path("update-shipping/", views.update_shipping, name="update_shipping"),
    path("update-billing-shipping/", views.update_billing_shipping, name="update_billing_shipping"),
    path("get-billing-shipping/", views.get_billing_shipping, name="get_billing_shipping"),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
