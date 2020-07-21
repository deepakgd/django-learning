from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View

from .forms import TodoForm
from .models import Todo

# Create your views here.
def home(request):
    return render(request, 'home.html')


def todo_create(request):
    if request.method == 'GET':
        todo_form = TodoForm()
        context = { 'form': todo_form }
        return render(request, 'todo_create.html', context)
    elif request.method == "POST":
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid:
            todo_form.save()
            return redirect("basics:home")
        else:
            return render(request, 'todo_create.html', { 'form': todo_form })

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todo_list.html', { 'todos': todos })

def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(None, instance=todo)
    return render(request, 'todo_edit.html', { 'form': form, 'id': pk })
    
def todo_update(request, pk):
    print(request.method)
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if(form.is_valid()):
            form.save()
            return redirect("basics:todo_list")
        else:
            return render(request, 'todo_edit.html', { 'form': form, 'id': pk })
    else:
        return redirect("basics:todo_list")

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect("basics:todo_list")


# class based view

class TodoListView(generic.ListView):
    template_name = "todo_list.html"
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.all()


class TodoCreateView(generic.CreateView):
    template_name = "todo_create_v2.html"
    form_class = TodoForm
    context_object_name = 'todo_form'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return '/todos/v2'

class TodoEditUpdateView(generic.UpdateView):
    model = Todo
    template_name = "todo_edit_v2.html"
    form_class = TodoForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        # print(self.kwargs)
        return '/todos/v2'

class TodoDeleteView(generic.DeleteView):
    template_name = "todo_delete.html"
    
    def get_object(self):
        id = self.kwargs.get("id")
        todo = get_object_or_404(Todo, pk=id)
        return todo

    def get_success_url(self):
        return '/todos/v2'