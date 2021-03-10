import datetime
import os.path

from django.shortcuts import render
from rest_framework.response import Response
from django.views.generic import DetailView
from django.views.generic.base import View
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.views import APIView
from rest_framework import status

from taskmanager.permissions import IsOwnerOrReadOnly
from taskmanager.serializer import TaskDetailSerializer, TaskListSerializer

from .models import Task


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskDetailSerializer
    def create(self, request):
        if int(request.data['user']) == request.user.id:
            serializer = TaskDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response( status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    def put(self, request, pk, format=None):
        task = Task.objects.get(id=pk)
        serializer = TaskDetailSerializer(task, data=request.data)
        if getattr(task, 'duedate') < datetime.date.today():
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        if getattr(task, 'done') == True:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        if getattr(task, 'duedate') < datetime.date.today():
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        task.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    

class TaskListView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.all().filter(user=request.user, done=0, duedate__gte = datetime.date.today())
            serializer = TaskListSerializer(tasks, many=True)
            return Response(serializer.data)
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        
       
    

