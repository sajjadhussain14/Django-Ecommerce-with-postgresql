from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "cart"

from . import views

urlpatterns = [
    path("", views.view_cart, name="viewCart"),
    path("add-to-cart", views.add_to_cart, name="add-to-cart"),
    path("clear-cart", views.clear_cart, name="clear_cart"),
    path("remove-cart-item", views.remove_cart_item, name="remove_cart_item"),
    path("update-cart-item", views.update_item_quantity, name="update_item_quantity"),
    path(
        "update-shipping", views.update_shipping_method, name="update_shipping_method"
    ),
    path("back-to-shop", views.back_to_shopping, name="back_to_shopping"),
    # add to wishlist
    path("add-to-wishlist", views.add_to_wishlist, name="add_to_wishlist"),
    path(
        "remove-from-wishlist", views.remove_from_wishlist, name="remove_from_wishlist"
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
