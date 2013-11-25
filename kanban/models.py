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
    REQUESTED = 'requested'
    TO_DO = 'to_do'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
        (REQUESTED, 'Requested'),
        (TO_DO, 'To do'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done'),
        (CONFIRMED, 'Confirmed'),
        (REJECTED, 'Rejected')
    )
    name = models.CharField(max_length=32,  choices=STATUS_CHOICES)
