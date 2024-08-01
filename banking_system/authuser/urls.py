from django.urls import path
from authuser import views

app_name = "authuser"

urlpatterns = [
    path("sign-up/", views.RegisterUserView, name="sign-up"),
    path("sign-in/", views.LoginUserView, name="sign-in"),
    path("sign-out/", views.LogoutUserView, name="sign-out"),
]
