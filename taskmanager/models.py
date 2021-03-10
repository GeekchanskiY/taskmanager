from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from django import forms
User = get_user_model()
import datetime

def check_date(value):
        if value < datetime.date.today():
            raise forms.ValidationError("DueDate cannot be in past!")
        return value
#Я очень долго тупил как правильно пользователя создать
class Task(models.Model):
    taskname = models.CharField(verbose_name='TaskName',max_length=200, db_index=True)
    priority = models.PositiveIntegerField(verbose_name='Priority',default = 1, validators=[MinValueValidator(1), MaxValueValidator(3)])
    duedate = models.DateField(verbose_name='DueDate',default=datetime.date.today, validators=[check_date])
    
    done = models.BooleanField(verbose_name='Status',default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.taskname
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"