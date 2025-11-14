# DRF Module
from rest_framework import serializers

# Directory Module
from .models import *


# Helpfull for validate task related data
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "project", "status", "due_date"]

    def validate(self, data):
        user = self.context.get('user')
        project_obj = data.get('project')
        title = data.get('title').strip()

        project = Project.objects.filter(id=project_obj.id).first()

        if not project.members.filter(email=user.email).exists():
            raise serializers.ValidationError({"user": "You have not a member of this project so not able to create a project related task"})
        
        if project.status == 'archived':
            raise serializers.ValidationError({"status":"This project is a archived project so it is already builded so only show for your refrence"})

        if Task.objects.filter(title=title, project=project.id).first():
            raise serializers.ValidationError({'title': "This title already added"})
        
        return data


# Helpfull for validate task related communication between project member
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Comment
        fields = ["task", "author", "text", "created_by"]