from django.urls import path
from .views import *

urlpatterns = [
    path("accounts/signup", RegisterAPI.as_view(), name="signup"),
    path("accounts/login", LoginApi.as_view(), name="login"),
    path("post", UserPostView.as_view(), name="login"),

]