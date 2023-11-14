from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "ecommerce"

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<slug:slug>/", views.category_page, name="category_page"),
    path("product/<slug:slug>/", views.product_page, name="product_page"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
