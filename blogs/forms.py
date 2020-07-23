from django import forms

from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "description", "active", "image",  "author"]

        # error message
        error_message = {
            'title': {
                'required': 'Title is required'
            },
            'description': {
                'required': 'description is required'
            },
            'author': {
                'required': 'Please select user to assign task'
            }
        }