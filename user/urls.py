from django.urls import path

from user.views import user


urlpatterns = [
    path("register/", user.register, name="register"),
    path("login/", user.login, name="login"),
]