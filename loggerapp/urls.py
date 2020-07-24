from django.urls import path

from . import views

app_name="loggerapp"

urlpatterns = [
    path("", views.loggertest, name="test_logs"),
    path("aws", views.awslogger, name="aws_test_logs")
]