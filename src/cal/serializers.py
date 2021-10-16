from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer
from .models import ProfileUser, CreateEvent, Holidays


class UserSerialiser(ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ('id', 'username', 'email', 'country')



class RegisterSerializer(ModelSerializer):
    class Meta:
        email = {'required': True}
        model = ProfileUser
        fields = ('id', 'username', 'email', 'password', 'country')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = ProfileUser.objects.create_user(validated_data['username'],
                                               email=validated_data['email'],
                                               password=validated_data['password'],
                                               country=validated_data['country'],)
        return user


class LoginSerializer(ModelSerializer):
    class Meta:
        model = ProfileUser
        email = {'required': True}
        fields = ['username', 'email', 'password']


class EventSerializer(ModelSerializer):
    class Meta:
        model = CreateEvent
        fields = ("title", "date_start", "date_finish", "reminder", 'notification')



class HolidaysSerializer(ModelSerializer):
    class Meta:
        model = Holidays
        fields = ('title', 'holiday_start', 'holiday_finish')


class ListEventSerializer(ModelSerializer):
    class Meta:
        model = CreateEvent
        fields = ['title', "date_start"]