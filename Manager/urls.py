from django.urls import path
from .views import *

urlpatterns = [
    path('task/all/', TaskView.as_view(), name='view-task'),
    path('task/search/', TaskSearchView.as_view(), name='search-task'),
    path('task/create/', TaskCreateView.as_view(), name='create-task'),
    path('task/delete/<str:name>/', TaskDeleteView.as_view(), name='delete-task'),
    path('task/edit/<str:name>/', TaskEditView.as_view(), name='task-edit'),

    path("task/add_photo/<int:pk>/", TaskPhotoCreateView.as_view(), name='create-task-photo'),
    path("task/delete_photo/<int:pk>/", TaskPhotoDeleteView.as_view(), name='delete-task-photo'),
    path('task/get_photo/<int:pk>/', TaskPhotoRetrieveView.as_view(), name='retrieve-task-photo'),

    path('theme/all/', ThemeView.as_view(), name='view-theme'),
    path('theme/create/', ThemeCreateView.as_view(), name='create-theme'),
    path('theme/delete/<str:name>/', ThemeDeleteView.as_view(), name='delete-theme'),
    path('theme/edit/<str:name>/', ThemeEditView.as_view(), name='theme-edit'),

    path('type_answer/all/', TypeAnswerView.as_view(), name='view-type_answer'),
    path('type_answer/create/', TypeAnswerCreateView.as_view(), name='create-type_answer'),
    path('type_answer/delete/<int:pk>/', TypeAnswerDeleteView.as_view(), name='delete-type_answer'),
    path('type_answer/edit/<int:pk>/', TypeAnswerEditView.as_view(), name='type_answer-edit'),
    path('type_answer/edit/<int:pk>/', TypeAnswerEditView.as_view(), name='type_answer-edit'),

    path('user/all/', UserListView.as_view(), name='view-user'),

    path('user_theme/create/', UserThemeCreateView.as_view(), name='user_theme-create'),

]
