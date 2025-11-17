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
        try:
            all_projects = Project.objects.all()
            page = self.paginate_queryset(all_projects)
            serializer = ProjectSerializer(page, many=True)
            return Response({
                "status": "success",
                "message": "Projects fetched successfully",
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


    # Create a new Project
    @handle_exception()
    def create(self, request, *args, **kwargs):
        user = request.user
        serializers = self.get_serializer(data=request.data, context={'user':user})
        serializers.is_valid(raise_exception=True)
        project = serializers.save()
        project.members.add(user.pk)
        return Response({
            "status": "success",
            "message": "Projects created successfully",
            "data": serializers.data
        }, status=status.HTTP_201_CREATED)
    
    
    # Used for getting detail of proejcts
    @handle_exception()
    @check_project_exists()
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        project = kwargs.get('project')

        if project.created_by != user and project.status == 'archived':
            return Response({
                "status": "error",
                "message": "You do not able to show this project bacause it is archived project so only created user able to show it."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Project retrieve successfully",
            "data":GetDetailProjectSerilaizer(project).data
        })

    
    # Update the project information    
    @handle_exception()
    @check_project_exists()
    def update(self, request, *args, **kwargs):
        user = request.user
        project = kwargs.get('project')

        if project.created_by != user:
            return Response({
                "status": "error",
                "message": "You do not permission to update this project"
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "PUT":
            serializers = self.get_serializer(project, data=request.data, context={'user': user})
        else:
            serializers = PartialUpdateProjectSerializer(project, data=request.data, partial=True)

        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({
            "status": "success",
            "message": "Project updated successfully",
            "data": serializers.data
        }, status=status.HTTP_200_OK)
        
    # Delete the project
    @handle_exception()
    @check_project_exists()
    def destroy(self, request, *args, **kwargs):
        user = request.user
        project = kwargs.get('project')

        if project.created_by != user:
            return Response({
                "status": "error",
                "message": "You do not permission to delete this project"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        project.delete()

        return Response({
                "status": "success",
                "message": "Project remove successfully",
                "data" : []
            }, status=status.HTTP_204_NO_CONTENT)
    

    # Assign member to a project
    @handle_exception()
    @check_project_exists()
    @action(detail=True, methods=["post"], url_name='add-member', url_path='add-member')
    def assign_member(self, request, *args, **kwargs):
        user = request.user
        project = kwargs.get('project')
        if project.created_by != user:
            return Response({
                "status": "error",
                "message": "You do not have permission to assign a new member"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializers = AssignMemberToProjectSerializer(data=request.data, context={'user':user, 'project':project})
        serializers.is_valid(raise_exception=True)
        return Response({
                "status": "success",
                "message": f"Assign member successfully for {project.name}",
                "data" : GetDetailProjectSerilaizer(project).data
            }, status=status.HTTP_200_OK)
    
    
    # Modify project status and mark as completed
    @handle_exception()
    @check_project_exists()
    @action(detail=True, methods=["post"], url_name='completed-project', url_path='complete')
    def mark_as_completed(self, request, *args, **kwargs):
        user = request.user
        project = kwargs.get('project')
        if project.created_by != user:
            return Response({
                "status": "error",
                "message": "You do not have permission to mark a project as complete"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if project.status == 'archived':
            return Response({
                "status": "success",
                "message": "Project already archived so it is already completed"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if project.status == 'completed':
            return Response({
                "status": "success",
                "message": "Project already completed"
            }, status=status.HTTP_400_BAD_REQUEST)
        project.status = 'completed'
        project.save(update_fields=['status'])
        return Response({
                "status": "success",
                "message": "Project completed successfully",
                "data": GetDetailProjectSerilaizer(project).data
            }, status=status.HTTP_200_OK)