# Django Module
from phonenumber_field.serializerfields import PhoneNumberField
import re

# DRF Module
from rest_framework import serializers

# Directory Module
from .models import *


# Build a Serializer for new users
class UserSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "phone", "dob"]
        extra_kwargs = {"password": {"write_only":True}}
        
    def validate(self, data):
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        username = User.get_username(data.get("email"), first_name, last_name)
        phone = str(data.get("phone", '')).strip()
        password = data.get('password')

        if not re.findall(r"[A-Z]", password):
            raise serializers.ValidationError({"password":"Atleat one Uppercase letter is required"})
        
        if len(password) < 8:
            raise serializers.ValidationError({"password":"Please make your password atleast 8 characte long"})

        data['first_name'] = first_name
        data['last_name'] = last_name
        data['username'] = username
        data['phone'] = phone

        return data
    

    def create(self, validated_data):
        # Remove non-hashable password
        password = validated_data.pop('password')
        user = User(**validated_data)
        # include a hashable password
        user.set_password(password)
        user.save()
        return user


# Build a seperate serializer for update a user information
class UserProfileUpdate(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone", "dob"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name).strip()
        instance.last_name = validated_data.get('last_name', instance.last_name).strip()
        instance.email = validated_data.get('email', instance.email).strip()
        instance.phone = validated_data.get('phone', instance.phone).strip()
        instance.dob = validated_data.get('dob', instance.dob)

        if instance.email:
            instance.username = User.get_username(instance.email, instance.first_name, instance.last_name)

        instance.save()
        return instance    


# UserLoginSerialize help us to check user enter detail is validate or not based on getting data from the database
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError({"user": "User does not exists"})
        
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Password does not match"})
        
        data['user'] = user

        return data


# Retrieve only access_token and refresh_token
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["access_token", "refresh_token"]


# Gettign the user details shortly
class UserInforSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


# Helpfull for getting the all user profile and also gettig the access_token and refresh_token
class SampleUserSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "phone", "dob", "tokens"]
        extra_kwargs = {"password": {"write_only":True}}
