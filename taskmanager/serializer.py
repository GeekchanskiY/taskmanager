from rest_framework import serializers
from django.core.exceptions import ValidationError
import datetime
from .models import Task
from .models import User

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('taskname', 'priority', 'duedate', 'done', 'user')
    def update(self, instance, validated_data):
        t = Task.objects.all()[instance.id-1]
        if (getattr(t,'taskname')) == '1234':
            raise ValidationError("YAY")
        if (getattr(t,'done')) == True:
            raise ValidationError("cant edit finished tasks")
        if getattr(t, 'duedate') < datetime.date.today():
            raise ValidationError("Cant edit tasks in past")
        instance.user = validated_data.get('user', instance.user)
        instance.taskname = validated_data.get('taskname', instance.taskname)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.duedate = validated_data.get('duedate', instance.duedate)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return instance
        
    


class TaskDetailSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    class Meta:
        model = Task
        fields = ('taskname', 'priority', 'duedate', 'done', 'user')
    


class TaskListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = '__all__'



