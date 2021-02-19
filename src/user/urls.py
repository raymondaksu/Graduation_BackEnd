from django.urls import path
from .views import RegisterView, ProfileView, UserGetUpdateDelete, ProfileListView, ChangePasswordView, PasswordTokenCheckAPI, ResetPasswordWithEmailView, SetNewPasswordAPIView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView),
    path('profile/', ProfileView),
    path('profile-list/', ProfileListView),
    path('edit/', UserGetUpdateDelete),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordWithEmailView.as_view(),
         name='reset-password'),
    path('reset-password/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='reset-password-confirm'),
    path('reset-password-complete/', SetNewPasswordAPIView.as_view(),
         name='reset-password-complete'),
]
