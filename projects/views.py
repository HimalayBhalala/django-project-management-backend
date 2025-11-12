# Django Module
from django.shortcuts import render

# DRF Module
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Directory Module
from .models import Project
from .serializers import *
from project_management.utils import handle_exception


class ProjectViewSet(viewsets.ModelViewSet):
    """
        ProjectViewSet is used for get list of project, create new project, get a detail of project, modify whole project information, modify few project information, provide a new member for complete early project and also able to change project status  
    """

    # Perform CRUD on Project so required a all project information
    def get_queryset(self):
        return Project.objects.all()
    
    # Set a default serializer for check validate data or not
    def get_serializer(self, *args, **kwargs):
        return 