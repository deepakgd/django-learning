from django import forms

from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "status", "is_completed", "user"]

        # custom error message , by defuat it will show this field is required now custom message will show
        error_messages = {
            'title': {
                'required': 'Title is required'
            },
            'description': {
                'required': 'Description is required'
            },
            'user': {
                'required': 'Please select user to assign task'
            }
        }

    # creating custom validation
    # clean_<field_name>
    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title');
        if "testing" in title:
            raise forms.ValidationError("This is not valid title because it contains testing keyword")
        else:
            return title