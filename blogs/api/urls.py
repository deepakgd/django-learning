from django.urls import path

from blogs.api import views

app_name = "blogs_api"

urlpatterns = [
    path('', views.get_all_blogs, name="list_blogs"),
    path('class/blogs', views.BlogList.as_view(), name="class_list"),
    path('create', views.create, name="create"),
    path('class/create', views.BlogCreate.as_view(), name="class_create"),
    path('update', views.update, name="update"),
    path('class/update', views.BlogUpdate.as_view(), name="class_update"),
    path('delete/<int:id>', views.delete, name="delete_blog"),
    path('class/delete/<int:id>', views.BlogDelete.as_view(), name="class_delete")
]