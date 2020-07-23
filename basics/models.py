from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=150, null=False)
    description = models.TextField()

    STATUS_CHOICES = (
        ("open", "Open"),
        ("close", "Close"),
        ("pending", "Pending")
    )

    status = models.CharField(max_length=7, choices=STATUS_CHOICES, null=False, default="open")

    is_completed = models.BooleanField(default=False)

    # CASCADE: When the referenced object is deleted, also delete the objects that have references to it 
    # (When you remove a blog post for instance, you might want to delete comments as well). SQL equivalent: CASCADE
    # user will automatically create column user_id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # to avoid todos_todos i mean appname_table name we can use this
    # this will create table name what u have mentioned 
    class Meta:
        db_table = "todos"


    # The __str__ method is useful for a string representation of the object, either when someone codes in str(your_object), or even when someone might do print(your_object). The __str__ method is one that should be the most human-readable possible, yet also descriptive of that exact object.
    # def __str__(self):
    #     return self.title