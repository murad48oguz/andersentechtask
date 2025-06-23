from rest_framework import permissions,viewsets
from .models import Task 
from .permissions import TaskPermission
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, TaskPermission]
    serializer_class = TaskSerializer
    pagination_class = PageNumberPagination


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Task.objects.all().order_by('-created_at')
        else:
            queryset = Task.objects.filter(user=self.request.user)
    
        if self.action == 'list':
            status = self.request.query_params.get('status')
            if status in [choice[0] for choice in Task.STATUS_CHOICES]:
                queryset = queryset.filter(status=status)
        return queryset

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'Done'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    
