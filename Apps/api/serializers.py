from rest_framework import serializers
from .models import User, Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.contrib.auth.models import Group, Permission


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ["id", "first_name","last_name", 'email', 'groups']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (["first_name","email", "last_name", 'password', 'password2'])

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            display_name="{}{}{}".format(validated_data["first_name"], " ", validated_data["last_name"]),
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=60, required=False)
    password = serializers.CharField(max_length=60, required=False)

    class Meta:
        fields = ('email', 'password')
        write_only_fields = ('password',)



class PostUserSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=60, required=True)
    content = serializers.CharField(max_length=500,required=True)
    class Meta:
        model = Post
        fields = ["author","title", "content"]




