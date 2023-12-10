from django.urls import path
from .views import *

urlpatterns = [
    path('userdone/<str:user_id>/', UserTasksView.as_view()),
    path('usernotdone/<str:user_id>/', UserNotDoneTasksView.as_view()),
    path('week/<str:user_id>/', UserTaskWeekView.as_view()),
]
