from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View

from .models import Blog
from .forms import BlogForm

class ListBlogs(generic.ListView):
    template_name = 'blogs.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.filter(active=True)

def create(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        return redirect("blogs:list")
    else:
        return render(request, 'create.html', { 'form': form })


class BlogCreate(generic.CreateView):
    template_name = "create.html"
    form_class = BlogForm
    context_object_name = 'form'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return '/blogs'

def update(request, id):
    blog = get_object_or_404(Blog, pk=id)
    form = BlogForm(None, instance=blog)
    if request.method == 'GET':
        return render(request, 'update.html', { 'form': form })
    elif request.method == 'POST':
        form = BlogForm(request.POST, files=request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blogs:list')
        else:
            return render(request, 'update.html', { 'form': form })


class BlogUpdate(generic.UpdateView):
    form_class = BlogForm
    template_name = "update.html"
    model = Blog

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return '/blogs'


def delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', { 'blog': blog })
    elif request.method == 'POST':
        blog.delete()
        return redirect('blogs:list')


class BlogDelete(generic.DeleteView):
    template_name = 'delete.html'
    model = Blog
    context_object_name = 'blog'

    def get_success_url(self):
        return '/blogs'

    