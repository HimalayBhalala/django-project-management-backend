# Django Module
from django.db import models

# DRF Module
from rest_framework import serializers

# Directory Module
from accounts.models import User
from projects.models import Project


TASK_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In_Progress'),
    ('completed', 'Completed')
]
# Create your models here.
# Used for manage the project tasks 
class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=15, choices=TASK_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = "task"

    def __str__(self):
        if self.assigned_to:
            return f"Task - {self.title} assigned to {self.assigned_to.username} for a {self.project.name}"
        return f"Task - {self.title} for a {self.project.name}"


# Usefull for connected all member for communicate the project related task and also helping to make a robust Project Management System
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        db_table = "comment"
