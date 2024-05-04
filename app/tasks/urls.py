'''
Tasks URL Configuration
'''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet)

app_name = 'task'

urlpatterns = [
    path('', include(router.urls)),
]
