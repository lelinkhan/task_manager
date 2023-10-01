from django.contrib import admin
from .models import Task, TaskPhoto


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'priority', 'is_complete', 'creation_datetime', 'last_update_datetime')


@admin.register(TaskPhoto)
class TaskPhotoAdmin(admin.ModelAdmin):
    list_display = ('task', 'photo')
