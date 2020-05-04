from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, DeleteTaskForm, ProjectForm, JournalForm, DeleteProjectForm
from django import forms

from taskmanager.models import Project, Task


@login_required
def home(request):
    return redirect('projects')


@login_required
def projects(request):
    current_user = request.user.username
    projects = request.user.project_set.all()
    return render(request, 'taskmanager/projects.html', {'user': current_user, 'projects': projects})


@login_required
def tasks(request, id):
    current_user = request.user.username
    project = get_object_or_404(Project, id=id)
    tasks = project.task_set.all()

    return render(request, 'taskmanager/tasks.html', {'user': current_user, 'tasks': tasks, 'project': project})


@login_required
def task(request, task_id):
    current_user = request.user.username
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    journals = task.journal_set.all()

    return render(request, 'taskmanager/task.html',
                  {'user': current_user, 'task': task, 'project': project, 'journals': journals})


@login_required
def newtask(request, id):
    project = get_object_or_404(Project, id=id)
    form = TaskForm(request.POST, initial={'project': project})
    members = project.Members
    form.fields["assigned"].queryset = members
    if form.is_valid():
        task = form.save(commit=False)
        task.project = project
        form.save()
        return redirect('tasks', id=project.id)

    return render(request, 'taskmanager/newtask.html', locals())


@login_required
def newproject(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('projects')

    return render(request, 'taskmanager/newproject.html', locals())


@login_required
def addcomment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = JournalForm(request.POST)
    if form.is_valid():
        journal = form.save(commit=False)
        journal.task = task
        journal.author = request.user
        journal.date = date.today()
        form.save()
        return redirect('task', task_id=task.id)

    return render(request, 'taskmanager/newcomment.html', locals())


@login_required
def modifytask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    form = TaskForm(request.POST or None, instance=task)

    context = {'form': form}

    members = project.Members

    form.fields["assigned"].queryset = members

    if form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()
        context = {'form': form}

        return redirect('tasks', id=project.id)

    return render(request, 'taskmanager/modifytask.html', context)

@login_required
def deleteproject(request, id):
    project_to_delete = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        form = DeleteProjectForm(request.POST, instance=project_to_delete)

        if form.is_valid():
            project_to_delete.delete()
            return redirect('projects')

    else:
        form = DeleteProjectForm(instance=project_to_delete)

    template_vars = {'form': form}
    return render(request, 'taskmanager/deleteproject.html', template_vars)




@login_required
def deletetask(request, task_id):
    task_to_delete = get_object_or_404(Task, id=task_id)
    project = task_to_delete.project

    if request.method == 'POST':
        form = DeleteTaskForm(request.POST, instance=task_to_delete)

        if form.is_valid():
            task_to_delete.delete()
            return redirect('tasks', id=project.id)

    else:
        form = DeleteTaskForm(instance=task_to_delete)

    template_vars = {'form': form}
    return render(request, 'taskmanager/deletetask.html', template_vars)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'taskmanager/signup.html', {'form': form})


from django.shortcuts import render

# Create your views here.
