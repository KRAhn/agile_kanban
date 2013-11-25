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
    STATUS_CHOICES = (
        (REQUESTED, 'requested'),
        (TO_DO, 'to_do'),
        (IN_PROGRESS, 'in_progress'),
        (DONE, 'done'),
        (CONFIRMED, 'confirmed'),
        (REJECTED, 'rejected')
    )
    name = models.CharField(max_length=32,  choices=STATUS_CHOICES)
