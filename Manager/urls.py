from django.urls import path
from .views import *

urlpatterns = [
    path('task/all/', TasksView.as_view(), name='view-task'),
    path('task/create/', TaskCreateView.as_view(), name='create-task'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete-task'),
    path('task/edit/<int:pk>/', TaskEditView.as_view(), name='task-edit'),

    path('theme/all/', ThemeView.as_view(), name='view-theme'),
    path('theme/create/', ThemeCreateView.as_view(), name='create-theme'),
    path('theme/delete/<int:pk>/', ThemeDeleteView.as_view(), name='delete-theme'),
    path('theme/edit/<int:pk>/', ThemeEditView.as_view(), name='task-edit'),
]
