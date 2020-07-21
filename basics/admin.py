from django.contrib import admin

from .models import Todo

# Register your models here.
# admin.site.register(Todo)

# you can also register like below methods 
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    # by default admin.site.register(Todo) will show like Todo objects. but now it will show as table
    list_display = ('title', 'description', 'status', 'is_completed', 'user_id')
