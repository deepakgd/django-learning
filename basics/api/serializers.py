from rest_framework import serializers

from basics.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    
    username = serializers.SerializerMethodField('get_username_from_user')
    
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "status", "is_completed", "user_id", "username"]

    def get_username_from_user(self, todo): 
        username = todo.user.username
        return username