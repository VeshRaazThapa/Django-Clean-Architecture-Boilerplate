from django.urls import path, re_path
from django.contrib.auth import views as auth

from ..views import auth as auth_views

auth_urlpatterns = [
    path('login', auth_views.user_login, name="login"),
    path('register', auth_views.register, name="register"),
    path('logout', auth_views.logout_view, name="logout"),
    # password reset
    path('password-reset', auth.PasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done', auth.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', auth.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # change password
]
