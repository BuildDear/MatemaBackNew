from django.urls import path
from .views import UserTasksView

urlpatterns = [
    path('tasks/<str:user_id>/', UserTasksView.as_view()),
]
