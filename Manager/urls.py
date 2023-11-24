from django.urls import path
from .views import *

urlpatterns = [
    path('task/all/', TaskView.as_view(), name='view-task'),
    path('task/search/', TaskSearchView.as_view(), name='search-task'),
    path('task/create/', TaskCreateView.as_view(), name='create-task'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete-task'),
    path('task/edit/<int:pk>/', TaskEditView.as_view(), name='task-edit'),

    path('tasks/createAnswer/<int:task_id>', TaskAnswerView.as_view(), name='add-task-answer'),

    path('theme/all/', ThemeView.as_view(), name='view-theme'),
    path('theme/create/', ThemeCreateView.as_view(), name='create-theme'),
    path('theme/delete/<int:pk>/', ThemeDeleteView.as_view(), name='delete-theme'),
    path('theme/edit/<int:pk>/', ThemeEditView.as_view(), name='theme-edit'),

    path('type_answer/all/', TypeAnswerView.as_view(), name='view-type_answer'),
    path('type_answer/create/', TypeAnswerCreateView.as_view(), name='create-type_answer'),
    path('type_answer/delete/<int:pk>/', TypeAnswerDeleteView.as_view(), name='delete-type_answer'),
    path('type_answer/edit/<int:pk>/', TypeAnswerEditView.as_view(), name='type_answer-edit'),

    path('user/all/', UserListView.as_view(), name='view-user'),
    path('type_answer/edit/<int:pk>/', TypeAnswerEditView.as_view(), name='type_answer-edit'),
]
