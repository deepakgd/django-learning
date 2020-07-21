from django.urls import path

from . import views;

app_name = "basics"

urlpatterns = [
    path("", views.home, name="home"),
    path("todo/create", views.todo_create, name="todo_create"),
    path("todos", views.todo_list, name="todo_list"),
    path("todo/<int:pk>", views.todo_edit, name="todo_edit"),
    path("todo/<int:pk>/update", views.todo_update, name="todo_update"),
    path("todo/<int:pk>/delete", views.todo_delete, name="todo_delete"),

    # todo class view
    path("todos/v2", views.TodoListView.as_view(), name="list_view_todo"),
    path("todo/v2/create", views.TodoCreateView.as_view(), name="create_view_todo"),
    path("todo/<int:pk>/v2/edit", views.TodoEditUpdateView.as_view(), name="edit_update_view"),
    path("todo/<int:id>/v2/delete", views.TodoDeleteView.as_view(), name="todo_delete_view")
]