from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "authentications"

from . import views

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("sign-up", views.sign_up_page, name="sign_up_page"),
    path("account", views.account_page, name="account_page"),
    path("logout/", views.logout_view, name="logout_view"),
    path("update-account/", views.update_account, name="update_account"),
     path("update-password/", views.update_password, name="update_password"),
    # for forget password
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
