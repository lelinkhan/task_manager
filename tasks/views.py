from django.db.models import Q
from .forms import RegistrationsFrom
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from .models import Task, TaskPhoto
from .forms import TaskForm, TaskPhotoForm


class FirstTemView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationsFrom()
        context = {'form': form}
        return render(request, 'registration.html', context)

    def post(self, request):
        form = RegistrationsFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! Registration Successfully!')
        context = {'form': form}
        return render(request, 'registration.html', context)


# Task List View
class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all().order_by('priority')
        tasksimg = TaskPhoto.objects.all()
        return render(request, 'task_list.html', {'tasks': tasks, 'tasksimg': tasksimg})


# # Task Creation View
class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        form1 = TaskPhotoForm()
        return render(request, 'task_creation.html', {'form': form, 'form1': form1})

    def post(self, request):
        form = TaskForm(request.POST, request.FILES)
        form1 = TaskPhotoForm(request.POST, request.FILES, prefix='photo')
        if form.is_valid():
            task = form.save(commit=False)  # Create a task instance without saving it to the database yet
            task.creator = request.user  # Set the task's creator to the current user
            task.save()  # Save the task with the creator assigned
            messages.success(request, 'Congratulations!! Form Submit Successfully!')
            return redirect(reverse('task-list'))
        return render(request, 'task_creation.html', {'form': form, 'form1': form1})


class TaskPhotoCreateView(View):
    def get(self, request):
        tasks = Task.objects.all()  # Fetch all available tasks
        return render(request, 'create_photo_task.html', {'tasks': tasks})

    def post(self, request):
        tasks = Task.objects.all()  # Fetch all available tasks
        form = TaskPhotoForm(request.POST, request.FILES, prefix='photo')
        if form.is_valid():
            task_id = request.POST.get('task_title')
            task = Task.objects.get(id=task_id)
            photo = form.save(commit=False)
            photo.task = task
            photo.save()
            return redirect('task-list')
        return render(request, 'create_photo_task.html', {'tasks': tasks, 'form': form})


# Task Details View
class TaskDetailView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        task = Task.objects.get(pk=task_id)
        taskimg = TaskPhoto.objects.get(pk=task_id)
        return render(request, 'task_details.html', {'task': task, 'taskimg': taskimg})


#
# # Task Update View
class TaskUpdateView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'task_update.html', {'form': form, 'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('task-list'))
        return render(request, 'task_update.html', {'form': form, 'task': task})


#
# # Task Deletion View
class TaskDeleteView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        return render(request, 'task_list.html', {'task': task})

    def post(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        task.delete()
        return redirect(reverse('task_list'))


class SearchItemView(View):
    template_name = 'search.html'

    def get(self, request):
        query = request.GET.get('query')
        if query:
            task = Task.objects.filter(Q(title__icontains=query))
            return render(request, self.template_name, {'task': task})
        else:
            return render(request, self.template_name, {'message': 'Sorry!! No Match!'})
