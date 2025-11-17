# Django Module
from django.urls import path, include

# DRF Module
from rest_framework.routers import DefaultRouter

# Include Directory Module
from . import views

# Gettign the built-in URL for perform CRUD
router = DefaultRouter()
router.register("accounts", views.UsersView, basename='user')

urlpatterns = [
    path("", include(router.urls))
]
