# DRF Module
from rest_framework import serializers

# Directory Module
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_by", "status"]
        extra_kwargs = {"id": {"read_only":True}}

    def validate(self, data):
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        
        if description: 
            if len(description) < 20:
                raise serializers.ValidationError({
                    "description": "Please include a atleast 20 words for description"
                })
            
        data['name'] = name
        data['description'] = description
        return data
    