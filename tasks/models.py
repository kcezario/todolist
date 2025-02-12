from django.db import models
from django.contrib.auth.models import User
from .constants import TaskStatus


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=1,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Task: {self.title}>"
