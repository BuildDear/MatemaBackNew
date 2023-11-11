from django.contrib import admin
from django.urls import path, include

from User import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', include('User.urls')),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/verify/<uidb64>/<token>/', views.activate_account, name='activate_account'),

    path('manager/', include('Manager.urls')),
]
