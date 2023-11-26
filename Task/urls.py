from django.urls import path
from .views import *

urlpatterns = [
    path('task_list/generate/', TaskListView.as_view(), name='task-list'),
]
