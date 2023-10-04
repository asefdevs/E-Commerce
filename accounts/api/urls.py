from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterApiView.as_view(),name='register'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('text/',views.Text.as_view(),name='text')

]
