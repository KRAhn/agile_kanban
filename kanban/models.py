from django.db import models


class Iteration(models.Model):
    goal = models.CharField(max_length=128)


class Task(models.Model):
    iteration = models.ForeignKey('Iteration')
    title = models.CharField(max_length=128)
    description = models.TextField()
    author = models.CharField(max_length=64)
    status = models.ForeignKey('Status')
    created_time = models.DateTimeField(auto_now_add=True)

    def dictify(self):
        return dict(
            id=self.id,
            iteration=self.iteration.goal,
            title=self.title,
            description=self.description,
            author=self.author,
            status=self.status.name,
            createdTime=self.created_time.strftime('%y-%m-%d %H:%M:%S')
        )


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
