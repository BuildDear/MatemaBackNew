from django.urls import path
from .views import *

urlpatterns = [
    path('list/generate/', TaskListView.as_view(), name='task-list-generate'),
    path('done/<str:username>/', TransferTaskView.as_view(), name='task-transfer'),
    path('statisic/<str:username>/', UserDoneTasksView.as_view(), name='task-done'),
]


