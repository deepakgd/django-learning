from django.urls import path

from account.api import views
from rest_framework.authtoken.views import obtain_auth_token

app_name="account_api"

urlpatterns = [
    path("", views.UserList.as_view(), name="list_user"),
    path("register", views.create_user, name="create_user"),
    path("register/class", views.CreateUser.as_view(), name="create_user_class"),
    path("login", obtain_auth_token, name="login"),
    path('customlogin', views.CustomLogin.as_view(), name="customlogin"),
    path('fullycustomlogin', views.CustomObtainAuthTokenView.as_view(), name="fullycustomlogin"),
    path('update', views.UpdateProfile.as_view(), name="update_profile"),
    path('update/v2', views.updateProfile, name="update_profile")
]