# Django Module
from django.urls import path, include

# DRF Module
from rest_framework.routers import DefaultRouter

# Directory Module
from . import views

# Getting built in router for perform CRUD related to tasks and also customize endpoints based on requirements
router = DefaultRouter()
router.register("tasks", views.TaskViewSet, basename='task')
router.register("comments", views.CommentViewSet, basename='comment')

# Include all tasks router url into a Project Management System
urlpatterns = [
    path("", include(router.urls))
]

