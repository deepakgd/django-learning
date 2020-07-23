from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path("", views.ListBlogs.as_view(), name="list"),
    path("create", views.create, name="create"),
    path("class/create", views.BlogCreate.as_view(), name="class_create"),
    path("update/<int:id>", views.update, name="update"),
    path("class/update/<int:pk>", views.BlogUpdate.as_view(), name="class_update"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("class/delete/<int:pk>", views.BlogDelete.as_view(), name="class_delete")
]