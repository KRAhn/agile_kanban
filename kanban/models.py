from django.db import models


class Status(models.Model):
    REQUESTED = 1
    TO_DO = 2
    IN_PROGRESS = 3
    DONE = 4
    CONFIRMED = 5
    REJECTED = 6
    STATUS_CHOICES = (
        (REQUESTED, 'Requested'),
        (TO_DO, 'To do'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done'),
        (CONFIRMED, 'Confirmed'),
        (REJECTED, 'Rejected')
    )
    name = models.CharField(choices=STATUS_CHOICES, max_length=32)


class Task(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    author = models.CharField(max_length=64)
    status = models.ForeignKey(Status)
    created_time = models.DateField(auto_now_add=True)