from django.urls import path

from . import views

app_name="loggerapp"

urlpatterns = [
    path("", views.loggertest, name="test_logs")
]