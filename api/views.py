from tasks.models import Task
from api.serializers import TaskSerializer
from rest_framework import viewsets


class UserListCreateView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer