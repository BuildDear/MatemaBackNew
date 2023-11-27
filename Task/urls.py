from django.urls import path
from .views import *

urlpatterns = [
    path('task_list/generate/', TaskListView.as_view(), name='task-list'),
    path('transfer-task/<str:username>/', TransferTaskView.as_view(), name='done-task'),
]
