from django.db import models


class TaskStatus(models.TextChoices):
    PENDING = "P", "Pending"
    IN_PROGRESS = "I", "In Progress"
    COMPLETED = "C", "Completed"
