from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterApiView.as_view(),name='register'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('profile/detail/', views.ProfileDetailApiView.as_view(), name='profile_detail'),
    path('profile/photo_update/',views.ChangeProfilePhoto.as_view(),name='photo-update'),
]
