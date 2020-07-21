from rest_framework import serializers

from basics.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "status", "is_completed", "user_id"]