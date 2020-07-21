from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(style={ 'input_type': 'password' }, write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_staff", "is_active", "is_superuser", "password", "confirm_password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }


    # particular field validation
    # def validate_password(self, value):
    #     print('password')
    #     print(value)
    #     # pwd = self.validated_data.get('password')
    #     # print(pwd)
    #     return self


    # all field validation
    def validate(self, data):
        password = data['password']
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password must match with Confirm password")
        
        return data


    # for class based view 
    # this will trigger if no create method in CreateUser class otherwise it will trigger that one
    # def create(self, *args, **kwargs):
        # return User.objects.create_user(email=self.validated_data['email'], username=self.validated_data['username'], password=self.validated_data['password'], first_name=self.validated_data['first_name'], last_name=self.validated_data['last_name'])


# update only first name, last name and password
class UserProfileSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={ 'input-type': 'password' }, write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "password", "confirm_password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }


     # all field validation
    def validate(self, data):
        password = data['password']
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password must match with Confirm password")
        
        return data