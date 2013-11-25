from django.db import models


class Iteration(models.Model):
    name = models.CharField(max_length=50)


class Task(models.Model):
    iteration = models.ForeignKey('Iteration')
    title = models.CharField(max_length=128)
    description = models.TextField()
    author = models.CharField(max_length=64)
    status = models.ForeignKey('Status')
    created_time = models.DateField(auto_now_add=True)


class Status(models.Model):
    REQUESTED = 1
    TO_DO = 2
    IN_PROGRESS = 3
    DONE = 4
    CONFIRMED = 5
    REJECTED = 6
    name = models.CharField(max_length=32)
