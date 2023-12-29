from django.urls import path
from User.views import UserPhotoView, \
    UserScoreView, UserGetTaskView
from User.service import check_user_active

urlpatterns = [

    path('check-user-active/<str:username>/', check_user_active, name='check-user-active'),

    path('score/', UserScoreView.as_view(), name='user-score'),
    path('task/<int:task_id>/', UserGetTaskView.as_view(), name='user-task-detail'),

    path('photo/', UserPhotoView.as_view(), name='user-photo'),
]
