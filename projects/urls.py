# Django Module
from django.urls import path, include

# DRF Module
from rest_framework.routers import DefaultRouter

# Directory Module
from . import views

# Getting built in router for perform CRUD and also customize endpoints based on requirements
router = DefaultRouter()
router.register("projects", views.ProjectViewSet, basename='project')

urlpatterns = [
    path("", include(router.urls))
]

