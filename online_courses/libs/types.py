from django.db import models

MARK_TYPES = (
    ('done', 'Done'),
    ('not done', 'Not done'),
    ('not provided', 'Not provided'),
    ('overdue', 'Overdue')
)


class RoleTypes(models.TextChoices):
    Teacher = 'Teacher'
    Student = 'Student'
