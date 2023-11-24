from django.urls import path
from User.views import UserPhotoCreateView, UserPhotoDeleteView

urlpatterns = [
    path('add_photo/', UserPhotoCreateView.as_view(), name='add-user-photo'),
    path('delete_photo/', UserPhotoDeleteView.as_view(), name='delete-user-photo'),
]