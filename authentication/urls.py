from django.urls import path
from .views import RegisterView,VerifyEmail, LoginAPIView, PasswordTokenCheckAPIView, RequestPasswordResetEmail,SetNewPasswordAPIView
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view() , name="register"),
    path('login/', LoginAPIView.as_view() , name="login"),
    path('verify-email/', VerifyEmail.as_view() , name="verify-email"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email" ),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm' ),
    path('password-reset-complete/',SetNewPasswordAPIView.as_view(), name='password-reset-complete' ),
    
    
]