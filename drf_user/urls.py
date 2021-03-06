from django.urls import path

from . import views


app_name = 'drf_user'

urlpatterns = [
    path('', views.UserView.as_view(), name='Get User Details'),
    # ex: api/user/login/
    path('login/', views.LoginView.as_view(), name='Login'),
    # ex: api/user/register/
    path('register/', views.RegisterView.as_view(), name='Register'),
    # ex: api/user/otp/
    path('otp/', views.OTPView.as_view(), name='OTP'),
    # ex: api/user/otpreglogin/
    path('otpreglogin/', views.OTPLoginView.as_view(),
         name='OTP-Register-LogIn'),
    # ex: api/user/isunique/
    path('isunique/', views.CheckUniqueView.as_view(), name='Check Unique'),
    # ex: api/user/account/
    path('account/', views.RetrieveUpdateUserAccountView.as_view(),
         name='Retrieve Update Profile'),
    # ex: api/user/password/reset/
    path('password/reset/', views.PasswordResetView.as_view(),
         name='Change User Password'),
    # ex: api/user/uploadImage/
    path('uploadimage/', views.UploadImageView.as_view(),
         name='Upload Photo'),
]
