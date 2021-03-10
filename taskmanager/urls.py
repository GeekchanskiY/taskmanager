from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from taskmanager.views import *
from . import views



urlpatterns = [
    path('task/create', TaskCreateView.as_view()),
    path('task/detail/<int:pk>/', TaskDetailView.as_view(), name = 'detail'),
    path('task/list', TaskListView.as_view())
    #router.urls
    ]