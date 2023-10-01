from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('taskmanager', views.UserListCreateView, basename='taskmanager')

urlpatterns = [
   path('', include(router.urls))
]