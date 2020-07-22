from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from account.api.serializers import UserSerializer, UserProfileSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(email=request.data['email'], username=request.data['username'], password=request.data['password'], first_name=request.data['first_name'], last_name=request.data['last_name'])
        user.save()
        token = Token.objects.get(user=user).key
        return Response(data={'message': 'User created Successfully', 'token': token })
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.CreateAPIView):
    model = User
    serializer_class = UserSerializer
    # by default this will validate and invoke create method of model or create method in serializer
    # that create method in serializer will return data what created. 
    # if you want to send custom message do below method

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(email=request.data['email'], username=request.data['username'], password=request.data['password'], first_name=request.data['first_name'], last_name=request.data['last_name'])
            user.save()
            token = Token.objects.get(user=user).key
            return Response(data={'message': 'User created Successfully', 'token': token})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # we can use this if token not created at at signup time
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': user.pk,
            'email': user.email
        })


class UpdateProfile(generics.UpdateAPIView):
    model = User
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(request.data['password'])
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.save()
        return Response({ 'message': "Profile updated successfully" })

# same above is done in functional method
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)
    user.set_password(request.data['password'])
    user.first_name = request.data.get('first_name')
    user.last_name = request.data.get('last_name')
    user.save()
    return Response({ 'message': 'Profile updated successfully' })
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)