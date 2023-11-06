from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='create-task'),
    path('tasks/<int:task_id>/', TaskDeleteView.as_view(), name='delete-task'),
    path('them/', ThemCreateView.as_view(), name='create-them'),
    path('them/', ThemDeleteView.as_view(), name='delete-them')
]
