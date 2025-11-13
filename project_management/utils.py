# DRF Module
from rest_framework import serializers, status
from rest_framework.response import Response
from projects.models import Project
from functools import wraps


# Custom Decorator used for check exception occure or not without affecting function logic
def handle_exception():
    def decorator(fun):
        @wraps(fun)
        def check_exception(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            # Show exception occure inside the serializer
            except serializers.ValidationError as e:
                return Response({
                    "status": "error",
                    "message": e.detail
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": f"Something went wrong: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return check_exception
    return decorator


def check_project_exists():
    def decorator(fun):
        @wraps(fun)
        def check(*args, **kwargs):
            id = kwargs.get('pk')
            project = Project.objects.filter(id=id).first()

            if not project:
                return Response({
                    "status": "success",
                    "message": "Requested project does not exists",
                    "data" : []
                }, status=status.HTTP_404_NOT_FOUND)

            kwargs['project'] = project            
            return fun(*args, **kwargs)
        return check
    return decorator