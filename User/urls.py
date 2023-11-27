from django.urls import path
from User.views import UserPhotoCreateView, UserPhotoDeleteView, UserPhotoRetrieveView, check_user_active


urlpatterns = [

    path('check-user-active/<str:username>/', check_user_active, name='check-user-active'),

    path('add_photo/', UserPhotoCreateView.as_view(), name='add-user-photo'),
    path('delete_photo/', UserPhotoDeleteView.as_view(), name='delete-user-photo'),
    path('user/get_photo/', UserPhotoRetrieveView.as_view(), name='retrieve-user-photo'),
]
