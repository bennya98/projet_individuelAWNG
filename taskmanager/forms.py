from django import forms
from .models import Task, Project, Journal


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        #fields = '__all__'
        exclude = ['project', ]

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
        fields = ['entry', ]


class DeleteTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

class DeleteProjectForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []