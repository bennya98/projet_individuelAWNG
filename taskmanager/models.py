from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    Name = models.CharField(max_length=120)
    Members = models.ManyToManyField(User)

    def __str__(self):
        return self.Name


class Status(models.Model):
    Name = models.CharField(max_length=120)

    def __str__(self):
        return self.Name


class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    Name = models.CharField(max_length=120)
    Description = models.CharField(max_length=500, blank=True)
    assigned = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.IntegerField(blank=True)
    status = models.ForeignKey('Status', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.Name


class Journal(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.CharField(max_length=1000)