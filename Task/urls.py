from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskView.as_view(), name='view-task'),
    path('', TaskCreateView.as_view(), name='create-task'),
    path('<int:task_id>/', TaskDeleteView.as_view(), name='delete-task'),
    path('theme/', ThemeView.as_view(), name='view-theme'),
    path('theme/', ThemeCreateView.as_view(), name='create-theme'),
    path('theme/<int:theme_id>/', ThemeDeleteView.as_view(), name='delete-theme')
]
