from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from taskmanager.models import Project, Task
from .forms import TaskForm, DeleteTaskForm, ProjectForm, JournalForm, DeleteProjectForm


# Redirect user to  the home screen if they simply enter /taskmanager as the url
# Login required for all views other than signup, user automatically redirected to login view if not already logged in
@login_required
def home(request):
    return redirect('projects')

# Main page
# Username sent to template as with all other pages so welcome message can be displayed
@login_required
def projects(request):
    current_user = request.user.username
    # Only displays projects that the user belongs to
    projects = request.user.project_set.all()
    return render(request, 'taskmanager/projects.html', locals())

# This view shows the tasks which make up a project. It requires the project id (id) as an input
@login_required
def tasks(request, id):
    current_user = request.user.username
    project = get_object_or_404(Project, id=id)
    tasks = project.task_set.all()

    return render(request, 'taskmanager/tasks.html', locals())

# Displays details of a specific task. Requires the task id (task_id) as an input
@login_required
def task(request, task_id):
    current_user = request.user.username
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    journals = task.journal_set.all()

    return render(request, 'taskmanager/task.html', locals())


# This view includes the form which allows the user to create a new task. It requires the id of the project it belongs
# to as an input
@login_required
def newtask(request, id):
    project = get_object_or_404(Project, id=id)
    form = TaskForm(request.POST, initial={'project': project})

    # Ensures a task can only be assigned to a member of the project
    members = project.Members
    form.fields["assigned"].queryset = members

    if form.is_valid():
        task = form.save(commit=False)

        # Project field has been excluded from form as the task must belong to the current project. Field must
        # therefore be pre-filled
        task.project = project

        form.save()

        # Redirect user to tasks page once new task has been submitted
        return redirect('tasks', id=project.id)

    return render(request, 'taskmanager/newtask.html', locals())


# View which contains form allowing user to create a new project
@login_required
def newproject(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        form.save()

        # Redirects user to projects page once form has been submitted
        return redirect('projects')

    return render(request, 'taskmanager/newproject.html', locals())


# View which allows user to add a comment on a specific task
@login_required
def addcomment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = JournalForm(request.POST)
    if form.is_valid():
        journal = form.save(commit=False)

        # Task, Author and Date fields have been excluded from comment form so they must be filled in automatically
        # with the task as the current task, the author as the current user's name and the date as the current date
        journal.task = task
        journal.author = request.user
        journal.date = date.today()

        form.save()

        # Redirects user to the page showing the specific task that the comment has been posted on
        return redirect('task', task_id=task.id)

    return render(request, 'taskmanager/newcomment.html', locals())

# This view allows the user to modify an existing task within a project
@login_required
def modifytask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    # Define form after getting chosen task means all fields are pre-filled with the existing data
    form = TaskForm(request.POST or None, instance=task)

    # Only members who belong to the project can be assigned a task
    members = project.Members
    form.fields["assigned"].queryset = members

    if form.is_valid():
        task = form.save(commit=False)

        # The project that a certain task belongs to cannot be modified. The Project field is excluded from the form
        # and is pre-filled
        task.project = project
        task.save()

        # Redirect user to the page of tasks within a project once task has been modified
        return redirect('tasks', id=project.id)

    return render(request, 'taskmanager/modifytask.html', locals())


# This view allows the user to delete a project
@login_required
def deleteproject(request, id):
    project_to_delete = get_object_or_404(Project, id=id)

    if request.method == 'POST':

        # Load blank form in order to prevent cross-site request forgery
        form = DeleteProjectForm(request.POST, instance=project_to_delete)

        if form.is_valid():
            project_to_delete.delete()

            # Redirect user to home screen once project has been deleted
            return redirect('projects')

    else:
        form = DeleteProjectForm(instance=project_to_delete)

    template_vars = {'form': form}
    return render(request, 'taskmanager/deleteproject.html', template_vars)


# This view allows the user to delete a task
@login_required
def deletetask(request, task_id):
    task_to_delete = get_object_or_404(Task, id=task_id)
    project = task_to_delete.project

    if request.method == 'POST':

        # Load blank form in order to prevent cross-site request forgery
        form = DeleteTaskForm(request.POST, instance=task_to_delete)

        if form.is_valid():
            task_to_delete.delete()

            # Redirect user to home screen once project has been deleted
            return redirect('tasks', id=project.id)

    else:
        form = DeleteTaskForm(instance=task_to_delete)

    template_vars = {'form': form}
    return render(request, 'taskmanager/deletetask.html', template_vars)


# Sign up page is the only view which doesn't require a log in for obvious reasons
def signup(request):
    if request.method == 'POST':

        # Form is a existing template imported from the library django.contrib.auth.forms
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            # Automatically log in the user once they have signed up and redirect them to the home screen
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'taskmanager/signup.html', locals())
