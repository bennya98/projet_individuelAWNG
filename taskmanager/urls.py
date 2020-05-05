from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('task/<int:task_id>', views.task, name='task'),
    path('task/new/<int:id>', views.newtask, name='newtask'),
    path('task/modify/<int:task_id>', views.modifytask, name='modifytask'),
    path('task/delete/<int:task_id>', views.deletetask, name='deletetask'),
    path('task/addcomment/<int:task_id>', views.addcomment, name='addcomment'),

    path('projects', views.projects, name='projects'),
    path('projects/<int:id>', views.tasks, name='tasks'),
    path('projects/new', views.newproject, name='newproject'),
    path('projects/delete/<int:id>', views.deleteproject, name='deleteproject'),

    path('signup', views.signup, name='signup'),
]