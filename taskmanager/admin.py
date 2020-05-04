from django.contrib import admin
from taskmanager.models import Project, Status, Task, Journal

admin.site.register(Project)
admin.site.register(Status)
admin.site.register(Task)
admin.site.register(Journal)