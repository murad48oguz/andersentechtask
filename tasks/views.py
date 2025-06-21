from rest_framework import permissions,viewsets
from .models import Task 
from .permissions import TaskPermission
from .serializers import TaskSerializer



class UserTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, TaskPermission]
    serializer_class = TaskSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
                return Task.objects.all()
        return Task.objects.filter(user=self.request.user)
    
    
