
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterUserView.as_view()),
    path('verify-otp/', views.VerifyOTPAndRegisterView.as_view()),
    path('login/', views.Loginuser.as_view()),
    path('resend/', views.ResendOTPView.as_view()),
    path('add_user/', views.AddUser.as_view()),
    path('get_users/', views.UserListView.as_view(), name='get-users'),
    path('users/<str:user_id>/', views.UserDetailView.as_view()),
]
