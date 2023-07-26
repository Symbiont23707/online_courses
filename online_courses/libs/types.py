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


class Weekdays(models.TextChoices):
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday = 'Sunday'


class Intervals(models.TextChoices):
    day = 'day',
    week = 'week',
    month = 'month'
