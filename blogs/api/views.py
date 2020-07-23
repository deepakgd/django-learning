from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

from blogs.models import Blog
from blogs.api.serializers import BlogsSerializer, BlogCreateSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogsSerializer(blogs, many=True)
    return Response(serializer.data)

class BlogList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # without pagination
    pagination_class = None


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    author = request.user
    blog = Blog(author=author)

    serializer = BlogCreateSerializer(blog, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class BlogCreate(generics.CreateAPIView):
    serializer_class = BlogCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    model = Blog

    def create(self, request, *args, **kwargs):
        user = request.user
        blog = Blog(author=user)
        serializer = BlogCreateSerializer(blog, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({ 'message': 'Blog created successfully' }, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request):
    author = request.user
    try:
        blog = Blog.objects.get(pk=request.data.get('id'))
    except Blog.DoesNotExist:
        return Response({ 'success': False, 'message': 'Blog not found' }, status=status.HTTP_404_NOT_FOUND)
    
    if author.id != blog.author.id:
        return Response({ 'success': False, 'message': 'You cannot edit other user blog' })
    
    serializer = BlogCreateSerializer(blog, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({ 'success': True, 'message': 'Blog updated successfully' }, status=status.HTTP_200_OK)


class BlogUpdate(generics.UpdateAPIView):
    model = Blog
    serializer_class = BlogCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        blog_id = self.request.data.get('id')
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({ 'success': False, 'message': 'Blog does not exists' })
        
        author = request.user

        if author.id != blog.author.id:
            return Response({ 'success': False, 'message': 'You cannot edit other user blog' })
        
        serializer = BlogCreateSerializer(blog, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({ 'success': True, 'message': 'Blog updated successfully' }, status=status.HTTP_200_OK)
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response({ 'success': False, 'message': 'Blog does not exists' })

    user = request.user
    if user.id != blog.author.id:
        return Response({ 'success': False, 'message': 'You cannot edit other user blog' }, status=status.HTTP_403_FORBIDDEN)

    blog.delete()
    return Response({ 'success': True, 'message': 'Blog deleted successfully' })

class BlogDelete(generics.DestroyAPIView):
    model = Blog
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BlogCreateSerializer


    def destroy(self, request, *args, **kwargs):
        blog_id = self.kwargs.get('id')
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({ 'success': False, 'message': 'Blog does not exists' })
        
        blog.delete()
        return Response({ 'success': True, 'message': 'Blog deleted successfully' })
        

    