from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset_password/', CustomResetPasswordView.as_view()),
    path('password_confirm/<uidb64>/', CustomPasswordConfirmView.as_view(), name='password_confirm'),
    path('vip/', VipView.as_view(),name='get_vip'),
    path('profile_update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('users/', UserListView.as_view(), name='get_users'),
    path('update_username/', UsernameUpdateView.as_view(), name='update_username'),
]