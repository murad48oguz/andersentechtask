from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from .views import UserTaskViewSet

router = DefaultRouter()
router.register(r'tasks',UserTaskViewSet,basename='task')

urlpatterns = [
    path('',include(router.urls))
]
