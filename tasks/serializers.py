# Django Module
from django.db.models import Q

# DRF Module
from rest_framework import serializers

# Directory Module
from .models import *


# Helpfull for validate task related data
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "project", "status", "due_date"]
        extra_kwargs = {"id": {"read_only": True}}

    def validate(self, data):
        user = self.context.get('user')
        project_obj = data.get('project') or self.instance.project
        title = data.get('title', '').strip()

        project = Project.objects.filter(id=project_obj.id).first()

        if not project.members.filter(email=user.email).exists():
            raise serializers.ValidationError({"user": "You have not a member of this project so not able to create or update a project related task"})
        
        if project.status == 'archived':
            raise serializers.ValidationError({"status":"This project is a archived project so it is already builded so only show for your reference"})

        if Task.objects.filter(title=title, project=project.id).first():
            raise serializers.ValidationError({'title': "This title already added"})
        
        return data
    

# Check task assigned user is valid or not
class TaskAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['assigned_to']

    def validate(self, data):
        task = self.context.get('task')
        user = self.context.get('user')
        assigned_user = data.get('assigned_to')

        project = Project.objects.filter(id=task.project.id).first()

        if not project.members.filter(email=user.email).exists():
            raise serializers.ValidationError({"user": "Requested user is not a member of an project so not able to getting a task"})
        
        if project.status == 'archived':
            raise serializers.ValidationError({"status":"This project is a archived project so it is already builded so only show for your reference"})
        
        if not project.members.filter(email=assigned_user.email).exists():
            raise serializers.ValidationError({"user": "Requested user is not a member of an project so not able to assigned a task"})
        
        if task.assigned_to:
            raise serializers.ValidationError({'assigned_to': f"This task is already assigned to {task.assigned_to.username}"})
        
        task.assigned_to = assigned_user
        task.save(update_fields=['assigned_to'])
        return data
    

# Get all Task related information
class DetailTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "project", "assigned_to", "status", "due_date"]
        extra_kwargs={"assigned_to": {"read_only": True}}

# Helpfull for validate task related communication between project member
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "task", "author", "text", "created_at"]
        extra_kwargs = {"id": {"read_only": True}}