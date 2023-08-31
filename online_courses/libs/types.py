from django.db import models

MARK_TYPES = (
    ('done', 'Done'),
    ('not done', 'Not done'),
    ('not provided', 'Not provided'),
    ('overdue', 'Overdue')
)


class MessageEmail:
    message = f'Lecture will be in '
    link = 'This is a link to the meeting for the lecture: '


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


class StatusLecture(models.TextChoices):
    active = 'active'
    inactive = 'inactive'


class WS:
    WS_LECTURE_NOTIFICATIONS = 'lecture_notification'


class MessageConfirmation:
    subject = 'Activate Your Account'
    accepted_confirmation = 'Thank you for your email confirmation.'
    invalid_link = 'Activation link is invalid!'
