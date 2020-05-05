from django import forms
from .models import Task, Project, Journal


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task

        # Project field excluded as a task is created within a given project so the field is pre-determined
        exclude = ['project', ]

        # Large text area for task description
        widgets = {
            'Description': forms.Textarea(),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal

        # other 3 fields are excluded as they are pre-determined variables (Task, Project, Date)
        fields = ['entry', ]

        # Large text area for comment
        widgets = {
            'entry': forms.Textarea(),
        }


class DeleteTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []


class DeleteProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = []