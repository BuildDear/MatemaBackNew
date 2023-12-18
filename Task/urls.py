from django.urls import path
from .views import *

urlpatterns = [
    path('list/generate/', GenerateTaskView.as_view(), name='task-list-generate'),
    path('list/get/<str:username>', TaskListView.as_view(), name='task-list-get'),
    path('done/<str:username>/', TransferTaskView.as_view(), name='task-transfer'),
    path('statistic/<str:username>/', UserDoneTasksView.as_view(), name='task-done'),
]


