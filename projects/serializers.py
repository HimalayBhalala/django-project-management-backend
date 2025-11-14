# DRF Module
from rest_framework import serializers

# Directory Module
from .models import *
from accounts.serializers import UserInforSerializer


# Helpfull for validate requested data while creating new project
class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserInforSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_by", "status"]
        extra_kwargs = {"id": {"read_only":True}}

    def validate(self, data):
        user = self.context.get('user')
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()

        project = Project.objects.filter(created_by=user.id, name=name).first()

        if project:
            raise serializers.ValidationError({"project": "Project already created"})
        
        if description: 
            if len(description) < 20:
                raise serializers.ValidationError({
                    "description": "Please include a atleast 20 words for description"
                })
            
        data['name'] = name
        data['description'] = description
        data['created_by'] = user
        
        return data
    

# Helpfull for include member inside the Project
class AssignMemberToProjectSerializer(serializers.Serializer):
    # Include a many user from the User table
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    def validate(self, data):
        members = data.get('members', [])
        user = self.context.get('user')
        project = self.context.get('project')
        if not members:
            raise serializers.ValidationError({'members':"Please Provide atleast one member for Project"})
        
        for member in members:
            if user.id == member.id and user.id == project.created_by.id:
                raise serializers.ValidationError({'members':"You have already member of this project because you have created project"})
            
            if project.members.filter(id=member.id).exists():
                raise serializers.ValidationError({"members": f"Member - {member.id} already exists"})
            project.members.add(member.id)

        project.save()
        return data
    

# Helpfull for getting the project detail and members information
class GetDetailProjectSerilaizer(serializers.ModelSerializer):
    members = UserInforSerializer(read_only=True, many=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    class Meta:
        model = Project
        fields = ["name", "description", "created_by", "members", "status"]
