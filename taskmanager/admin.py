from django.contrib import admin
from .models import Task

# Register your models here.
class taskmanageradmin(admin.ModelAdmin):
    list_display = ('id', 'taskname', 'priority', 'duedate', 'done')
    list_display_links = ('id', 'taskname')
    search_fields = ('id', 'taskname')
    filter = ('done',)
    list_editable = ('done',)

admin.site.register(Task, taskmanageradmin)