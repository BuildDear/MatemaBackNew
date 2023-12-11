from django.urls import path
from .views import *

urlpatterns = [
    path('task/done/<str:username>/', UserTasksView.as_view(),  name='user-task-done'),
    path('task/not-done/<str:username>/', UserNotDoneTasksView.as_view(), name='user-task-not-done'),
    path('task/week/<str:username>/', UserTaskWeekView.as_view(), name='user-task-week'),
]
