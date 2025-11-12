from django.db import models
from accounts.models import User

# Create your models here.

STATUS_CHOICES = [
    ('active','Active'),
    ('completed', 'Completed'),
    ('archived', 'Archived')
]

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='project_created_by')
    members = models.ManyToManyField(User, related_name='project_member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = "project"

    def __str__(self):
        if self.created_at:
            return f"Project - {self.name} created by {self.created_at.username}"
        return f"Project - {self.name}"