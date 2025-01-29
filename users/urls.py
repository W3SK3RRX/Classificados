# users/urls.py
from django.urls import path

from users.views import RegisterView, LoginView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Rota para registro
    path('login/', LoginView.as_view(), name='login'),  # Rota para login
    path('logout/', LogoutView.as_view(), name='logout'),  # Rota para logout
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),  # Solicitação de redefinição de senha
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Confirmação de redefinição de senha
]
