from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User

from basics.models import Todo
from basics.api.serializers import TodoSerializer, TodoSerializerUpdate


@api_view(['GET'])
def get_todo(request, id):
    try:
        todo = Todo.objects.get(pk=id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TodoSerializer(todo)
    return Response(serializer.data)

# only authorized user can access this
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_todo(request):
    print(request.user) # it contains user data
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todo(request):

    # currently hard coded becuase no auth token feature implemented
    user = request.user
    todo = Todo(user=user)

    serializer = TodoSerializer(todo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_todo(request, id):

    try:
        todo = Todo.objects.get(pk=id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = TodoSerializer(todo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo(request, id):
    try:
        todo = Todo.objects.get(pk=id)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    operation = todo.delete()
    if operation:
        return Response(data={ "message": "todo deleted successfully" })
    else:
        return Response(data={ "message": "Operation todo delete failed" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000

class TodoList(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [TokenAuthentication]    
    permission_classes = [IsAuthenticated]
    # if you want to override default pagination u can use below
    # by default pagination setted in settings is PageNumberPagination now i override to LimitOffsetPagination
    # pagination_class = LimitOffsetPagination

    # here custom class pagination
    # pagination_class = CustomPagination

    # if you dont want pagination use like below
    # pagination_class = None



class TodoListWithSearchFilter(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'status', 'description', 'user__username']


class TodoCreate(generics.CreateAPIView):
    model = Todo
    serializer_class = TodoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        user = request.user
        todo = Todo(user=user)
        serializer = TodoSerializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({ 'message': "Todo created successfully" })


class TodoUpdate(generics.UpdateAPIView):
    model = Todo
    serializer_class = TodoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.request.data.get('id')
        return Todo.objects.get(pk=id)
