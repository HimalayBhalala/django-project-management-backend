# Django module
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Build a Custom User Class for Authentication and Authorization
class User(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    @staticmethod
    def get_username(email, first_name=None, last_name=None):
        if first_name and last_name:
            return f"{first_name} {last_name}"
        custom_username = email.split('@')[0]
        return custom_username

    def __str__(self):
        return f"User {self.pk} - {self.email}"


# Keep Track of User login records and also help us for future while blocked the user
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    access_token = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        db_table = "token"