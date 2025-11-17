# DRF Module
from rest_framework_simplejwt.tokens import RefreshToken

# Directory Module
from .serializers import TokenSerializer
from .models import Token

# Generate a access token and refresh token for authenticated user
def get_token(user):
    
    tokens = RefreshToken.for_user(user)
    # Create token entry if not exists and update tokens if already exists
    token, create = Token.objects.update_or_create(
        user=user, 
        defaults={   
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens),
        }
    )
    # Return a Json response
    return TokenSerializer(token).data