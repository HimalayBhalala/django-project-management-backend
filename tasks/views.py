# Django Module
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend                                   

# DRF Module
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Directory Module
from .models import Project
from .serializers import *
from .utils import CommentFilter
from project_management.utils import handle_exception, check_task_exists


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
            serializer = TaskDetailSerializer(page, many=True)
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
    

    # Used for getting detail of task
    @handle_exception()
    @check_task_exists()
    def retrieve(self, request, *args, **kwargs):
        task = kwargs.get('task')
        return Response({
            "status": "success",
            "message": "task retrieve successfully",
            "data":DetailTaskSerializer(task).data
        }, status=status.HTTP_200_OK)


    # Update the task information    
    @handle_exception()
    @check_task_exists()
    def update(self, request, *args, **kwargs):
        user = request.user
        task = kwargs.get('task')
        if request.method == "PUT":
            serializers = self.get_serializer(task, data=request.data, context={'user': user})
        else:
            serializers = self.get_serializer(task, data=request.data, context={'user': user}, partial=True)

        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({
            "status": "success",
            "message": "Task modify successfully",
            "data": serializers.data
        }, status=status.HTTP_200_OK)
        
        
    # Deleting task
    @handle_exception()
    @check_task_exists()
    def destroy(self, request, *args, **kwargs):
        user = request.user
        task = kwargs.get('task')

        if not task.project.members.filter(email=user.email).exists():
            return Response({
                "status":"error",
                "message": "You have not a member of this project so not able to cdelete a project related task"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if task.status == 'archived':
            return Response({
                "status":"error",
                "message":"This project is a archived project so it is already builded so not able to delete this task"
            }, status=status.HTTP_400_BAD_REQUEST)

        task.delete()

        return Response({
                "status": "success",
                "message": "Task remove successfully",
                "data" : []
            }, status=status.HTTP_204_NO_CONTENT)

    
    # Assign task to user
    @handle_exception()
    @check_task_exists()
    @action(detail=True, methods=['post'], url_name='assign_user', url_path='assign')
    def task_assign_to_user(self, request, *args, **kwargs):
        user = request.user
        task = kwargs.get('task')
        serializers = TaskAssignSerializer(data=request.data, context={'user':user, "task":task})
        serializers.is_valid(raise_exception=True)
        return Response({
            "status": "success",
            "message": "Task assigned successfully",
            "data": DetailTaskSerializer(task).data
        }, status=status.HTTP_200_OK)
    

    # Mark as a Completed Task
    @handle_exception()
    @check_task_exists()
    @action(detail=True, methods=['post'], url_name='mark-as-complete', url_path='complete')
    def mark_as_completed(self, request, *args, **kwargs):
        user = request.user
        task = kwargs.get('task')

        project = Project.objects.filter(id=task.project.id).first()

        if not project.members.filter(email=user.email).exists():
            return Response({
                "status":"error",
                "message": "Requested user is not a member of an project so not able to mark as a completed task"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if project.status == 'archived':
            return Response({
                "status":"error",
                "message":"This project is a archived project so it is already builded so only show for your reference"
            }, status=status.HTTP_400_BAD_REQUEST)

        if task.status == 'completed':
            return Response({
                "status":"error",
                "message": "Task already completed"
            }, status=status.HTTP_400_BAD_REQUEST)

        task.status = 'completed'
        if not task.assigned_to:
            task.assigned_to = user
            task.save(update_fields=['status', 'assigned_to'])
        else:
            task.save(update_fields=['status'])

        return Response({
            "status": "success",
            "message": "Task completed successfully",
            "data": DetailTaskSerializer(task).data
        }, status=status.HTTP_200_OK)


    # All Project Management Users are able to create a comment based on tasks so it is helping us to develop the project based on their idea's and conversation
    @handle_exception()
    @check_task_exists()
    @action(detail=True, methods=['get', 'post'], url_name='get-or-create-comment', url_path='comments')
    def get_or_create_comment(self, request, *args, **kwargs):
        user = request.user
        task = kwargs.get('task')
        data = request.data

        if request.method == "GET":
            comments = Comment.objects.filter(task=task)
            return Response({
                "status": "success",
                "message": "Comment retrieve successfully",
                "data": CommentInfoSerializer(comments, many=True).data
            }, status=status.HTTP_200_OK)

        data['task'] = task.id
        serializers = CommentSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(author=user)
        return Response({
            "status": "success",
            "message": "Comment added successfully",
            "data": serializers.data
        }, status=status.HTTP_201_CREATED)


# Helpfull for getting all the comment and also able to filter it
class CommentViewSet(viewsets.ModelViewSet):
    
    # Only authenticated user can able to show comments
    permission_classes = [IsAuthenticated]
    
    # Perform operation on Comment Model
    queryset = Comment.objects.all()

    # Serializer for getting field based information
    serializer_class = TaskCommentSerilaizer

    # Django Built in Filter
    filter_backends = [DjangoFilterBackend]

    # Include fields set based filtering
    filterset_class = CommentFilter