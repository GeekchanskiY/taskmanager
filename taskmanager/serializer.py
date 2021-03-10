from rest_framework import serializers
from .models import Task
from .models import User

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('taskname', 'priority', 'duedate', 'done', 'user')


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

#Да, они дублируются, но раньше у меня была какая-то тактика и я ёё придерживался
