# Django Module
import django_filters

# Directory Module
from .models import Comment


# Build a Custom filter for filtering the project, assigned_to and status wise getting data
class CommentFilter(django_filters.FilterSet):

    project = django_filters.NumberFilter(field_name='task__project_id')
    assigned_to = django_filters.NumberFilter(field_name="task__assigned_to_id")
    status = django_filters.CharFilter(field_name="task__status")

    class Meta:
        model = Comment
        fields = ["project", "assigned_to", "status"]