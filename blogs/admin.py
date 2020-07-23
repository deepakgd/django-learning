from django.contrib import admin

from .models import Blog

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'image', 'active' ,'created_at', 'updated_at')