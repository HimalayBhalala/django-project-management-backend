# Django Module
from django.shortcuts import render

# DRF Module
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Directory Module
from .models import Project
from .serializers import *
from project_management.utils import handle_exception


class ProjectViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]

    """
        ProjectViewSet is used for get list of project, create new project, get a detail of project, modify whole project information, modify few project information, provide a new member for complete early project and also able to change project status  
    """

    # Perform CRUD on Project so required a all project information
    def get_queryset(self):
        return Project.objects.all()
    
    # Set a default serializer for check validate data or not
    def get_serializer(self, *args, **kwargs):
        return ProjectSerializer(*args, **kwargs)
    
    # Get all the project
    def list(self, request):
        all_projects = Project.objects.filter(created_by=request.user)
        serializer = ProjectSerializer(all_projects, many=True)
        return Response({
            "status": "success",
            "message": "All projects fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # Create a new Project
    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['created_by'] = user.pk
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({
            "status": "success",
            "message": "Projects created successfully",
            "data": serializers.data
        }, status=status.HTTP_201_CREATED)
    