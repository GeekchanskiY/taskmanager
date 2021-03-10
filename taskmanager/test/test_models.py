import json

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import CoreAPIClient
from rest_framework.test import force_authenticate
from taskmanager.models import Task
from taskmanager.views import TaskDetailView

import datetime
from datetime import timedelta

#P.S. я знаю что в идеале это в идеале разбивается на функции, ноооооо... \_(*.*)_/    
class TestCreateModels():
    
    def test_allinone(self):
        #создание клиентов
        client1 = APIClient()
        client2 = APIClient()
        userdata1 = {"username":"testuser1","email":"test@gaga.mlg","first_name": "123","last_name": "321","password":"megastrongpassword","password_confirm":"megastrongpassword"}
        userdata2 = {"username":"testuser2","email":"test@gaga.mlg","first_name": "123","last_name": "321", "password":"megastrongpassword","password_confirm":"megastrongpassword"}
        task1 = {"taskname": "123","priority": 2, "duedate": datetime.date.today(),"done": 0,'user':1}
        task2 = {"taskname": "123", "priority": 2,"duedate": datetime.date.today(),"done": 0,'user':1}
        task3 = {"taskname": "12345","priority": 3, "duedate": datetime.date.today(),"done": 0,'user':1}
        another_users_task = {"taskname": "12345","priority": 3, "duedate": datetime.date.today(),"done": 0,'user':1}
        wrongdatetask = {"taskname": "123","priority": 2,"duedate": datetime.date.today() - timedelta(days=1),"done": 0,'user':1}
        wrongpropritytask = {"taskname": "12345", "priority": 666,"duedate": datetime.date.today(),"done": 0,'user':1 }
        wrongusertask = {"taskname": "123","priority": 2, "duedate": datetime.date.today(),"done": 0,'user':2}
        
        register1 = client1.post('/accounts/register/', userdata1)
        assert register1.status_code == status.HTTP_201_CREATED
        log1 = client1.login(username='testuser1', password='megastrongpassword')
        assert log1 == True
        #creating task check
        response1 = client1.post('/api/v1/taskmanager/task/create',task1)
        assert response1.status_code == status.HTTP_201_CREATED
        #task date validation
        Wrong_date_response = client1.post('/api/v1/taskmanager/task/create',wrongdatetask)
        assert Wrong_date_response.status_code == status.HTTP_400_BAD_REQUEST
        #task with wrong user validation
        Wrong_user_response = client1.post('/api/v1/taskmanager/task/create',wrongusertask)
        assert Wrong_date_response.status_code == status.HTTP_400_BAD_REQUEST
        
        #checks if list doesnt show another users task
        client1.post('/api/v1/taskmanager/task/create',task2)
        client1.post('/api/v1/taskmanager/task/create',task3)
        client2.post('/api/v1/taskmanager/task/create',another_users_task)

        get = client1.get('/api/v1/taskmanager/task/list')
        assert len(get.data) == 3

        put = client1.put('/api/v1/taskmanager/task/detail/2/',{"taskname": "321", "priority": 1,"duedate": datetime.date.today(),"done": 1,'user':1})
        assert put.status_code == status.HTTP_202_ACCEPTED

        #checks if list doesnt shows done task
        get = client1.get('/api/v1/taskmanager/task/list')
        assert len(get.data) == 2

        assert get.data[0].get('taskname') == '123'
        assert get.data[1].get('user') == 1
   