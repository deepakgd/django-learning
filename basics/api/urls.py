from django.urls import path

from basics.api import views

app_name = "basics_api"

urlpatterns = [
    path("", views.get_all_todo, name="get_all_todos"),
    path("<int:id>", views.get_todo, name="get_todo"),
    path("create", views.create_todo, name="create_todo"),
    path("<int:id>/update", views.update_todo, name="update_todo"),
    path("<int:id>/delete", views.delete_todo, name="delete_todo"),

    # generic class based view for api
    path("class/todos", views.TodoList.as_view(), name="get_all_todo_v2"),
    path("class/todos/filter", views.TodoListWithSearchFilter.as_view(), name="todo_with_filter")
]