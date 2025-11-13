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
from project_management.utils import handle_exception, check_project_exists


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
    @handle_exception()
    def list(self, request):
        all_projects = Project.objects.filter(created_by=request.user)
        serializer = ProjectSerializer(all_projects, many=True)
        return Response({
            "status": "success",
            "message": "All projects fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # Create a new Project
    @handle_exception()
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
    
    # Used for getting detail of proejcts
    @handle_exception()
    @check_project_exists()
    def retrieve(self, request, *args, **kwargs):
        project = kwargs.get('project')
        return Response({
            "status": "success",
            "message": "Project retrieve successfully",
            "data": self.get_serializer(project).data
        })
    
    @handle_exception()
    @check_project_exists()
    def update(self, request, *args, **kwargs):
        project = kwargs.get('project')
        
        if request.method == "PUT":
            serializers = self.get_serializer(project, data=request.data)
        else:
            serializers = self.get_serializer(project, data=request.data, partial=True)

        serializers.is_valid(raise_exception=True)
        serializers.save(created_by=request.user)
        return Response({
            "status": "success",
            "message": "Project updated successfully",
            "data": serializers.data
        }, status=status.HTTP_200_OK)
        
    @handle_exception()
    @check_project_exists()
    def destroy(self, request, *args, **kwargs):
        project = kwargs.get('project')

        project.delete()

        return Response({
                "status": "success",
                "message": "Project remove successfully",
                "data" : []
            }, status=status.HTTP_204_NO_CONTENT)
    
    @handle_exception()
    @check_project_exists()
    @action(detail=True, methods=["post"], url_name='add-member', url_path='add-member')
    def assign_member(self, request, *args, **kwargs):
        project = kwargs.get('project')
        pass

