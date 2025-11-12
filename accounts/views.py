# Django Module
from django.shortcuts import render

# DRF Module
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Directory Module
from .serializers import *
from .token_generation import get_token
from project_management.utils import handle_exception

# Create your views here.
class UsersView(viewsets.ModelViewSet):
    """
        UsersView is a viewset for retrieve, create, fully_update, partial_update, and delete user data.      
    """
    # Getting all the include users information
    def get_queryset(self):
        return User.objects.all()
    
    # Check user sended data is validated or not
    def get_serializer_class(self):
        return UserSerializer
    
    # Override global JwtAuthentication(inside the settings) for register and login
    def get_authenticators(self):
        if self.request.path.endswith("/register/") or self.request.path.endswith("/login/"):
            return []
        return super().get_authenticators()
    
    # Only authenticated user able to view it's profile
    def get_permissions(self):
        if self.request.path.endswith("/me/"):
            return [IsAuthenticated()]
        return super().get_permissions()

    @handle_exception()
    @action(detail=False, methods=["post"], url_name="register", url_path="register")
    def user_registration(self, request):
        """
            Register a new user for able access the Project Management System features
        """
        # Provide entire request data to serializer for check sended data is validate or not
        serializers = UserSerializer(data=request.data)
        # If all data is validate so not raise the exception
        serializers.is_valid(raise_exception=True)
        # If not raise the exception so data is save correctly into the database table
        serializers.save()
        return Response({
            "status": "success",
            "message": "Registration success",
            "data": serializers.data
        }, status=status.HTTP_201_CREATED)
    
    @handle_exception()
    @action(detail=False, methods=["post"], url_name="login", url_path="login")
    def user_login(self, request):
        """
            User included valid email and password so getting the access_token and able to 
            use the Project Management System features
        """
        serializers = UserLoginSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializers.validated_data.get('email')).first()
        token = get_token(user)
        return Response({
            "status": "success",
            "message": "Login success",
            "data": {
                "user": UserSerializer(user).data,
                "token": token
            }
        }, status=status.HTTP_200_OK)
       
    @handle_exception()
    @action(detail=False, methods=["get", "patch"], url_name='profile', url_path='me')
    def user_get_profile(self, request):
        """
            Get the user profile information if validate authentication token included and also able to update their profile
        """
        user = request.user
        if request.method == "GET":
            return Response({
                "status":"success",
                "message": "Profile getting successfully",
                "data": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        # For Update Profile
        serializers = UserProfileUpdate(user, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({
            "status":"success",
            "message": "Profile updated successfully",
            "data": serializers.data
        }, status=status.HTTP_200_OK)
