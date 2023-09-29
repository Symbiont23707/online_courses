from django.db import models

from config import settings

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


class MessageUser:
    user_not_exist = 'User with this email does not exist.'
    reset_password = 'Reset Password'
    click_to_reset_link = 'Click the following link to reset your password: '
    password_refreshed = 'Your password has been refreshed'
    invite_notification = 'Invite Notification'
    invite_to_register = 'Click the following link to register in online_courses: '


class UserUrls:
    reset_url = f'{settings.HOST}/api/v1/users/reset-password/'
    change_url = f'{settings.HOST}/api/v1/users/change-password/?'
    invite_url = f'{settings.HOST}/api/v1/users/register/?'

class CourseUrls:
    course_api_view_url = f'{settings.HOST}/api/v1/courses/'

class HomeTaskUrls:
    home_task_api_view_url = f'{settings.HOST}/api/v1/home_tasks/'

class HomeTaskResultUrls:
    home_task_result_api_view_url = f'{settings.HOST}/api/v1/home_tasks/completed/'

class LectureUrls:
    lecture_api_view_url = f'{settings.HOST}/api/v1/lectures/'

class ZoomUrls:
    zoom_webhook_url = f'{settings.HOST}/webhook/event_notification/'