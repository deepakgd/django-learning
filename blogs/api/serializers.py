from rest_framework import serializers

from blogs.models import Blog


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_author_from_user')
    email = serializers.SerializerMethodField('get_author_email_from_user')

    class Meta:
        model = Blog
        fields = ['name', 'email']

    def get_author_from_user(self, author):
        return author.username

    def get_author_email_from_user(self, author):
        return author.email

class BlogsSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'active', 'image', 'created_at', 'author']

class BlogCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'active', 'image']

