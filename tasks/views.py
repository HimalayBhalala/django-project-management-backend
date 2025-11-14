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


class TaskViewSet(viewsets.ModelViewSet):

    """
        Helpfull for perform task related operation like get all tasks, create new task, get detail of task, modify all detail of task, modify few detail of task, delete the task, assign new user for complete the task, user can able to mark as completed if task is done, user can able to shown all comment and also able to create a new comment
    """

    # Only authenticated user can able to access below APIs
    permission_classes = [IsAuthenticated]

    # Perform CRUD on Project so required a all tasks information
    def get_queryset(self):
        return Task.objects.all()
    
    # Set a default serializer for check validate data or not
    def get_serializer(self, *args, **kwargs):
        return TaskSerializer(*args, **kwargs)
    
     # Get all the Task
    @handle_exception()
    def list(self, request):
        try:
            tasks = Task.objects.all()
            page = self.paginate_queryset(tasks)
            serializer = TaskSerializer(page, many=True)
            return Response({
                "status": "success",
                "message": "Tasks getting successfully",
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "status": "success",
                "message": "No data found",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
        

    # Create a new Task
    @handle_exception()
    def create(self, request, *args, **kwargs):
        user = request.user
        serializers = self.get_serializer(data=request.data, context={'user':user})
        serializers.is_valid(raise_exception=True)
        task = serializers.save()
        return Response({
            "status": "success",
            "message": "Task created successfully",
            "data": TaskSerializer(task).data
        }, status=status.HTTP_201_CREATED)
    