from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Login


class Userlogin(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'Name',
            'Contact'
        )


class LoginDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class ForgotSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
