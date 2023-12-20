from django.urls import path
from User.views import UserPhotoView, check_user_active, \
    UserScoreView, UserGetTaskView

urlpatterns = [

    path('check-user-active/<str:username>/', check_user_active, name='check-user-active'),

    path('score/', UserScoreView.as_view(), name='user-score'),
    path('task/<int:task_id>/', UserGetTaskView.as_view(), name='user-task-detail'),

    path('photo/', UserPhotoView.as_view(), name='user-photo'),
]
