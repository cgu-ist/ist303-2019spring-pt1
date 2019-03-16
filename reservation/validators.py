import datetime
from django.core.exceptions import ValidationError


def validate_start_time(start_time):
    validate_time('start_time', start_time)


def validate_end_time(end_time):
    validate_time('end_time', end_time)


def validate_time(name, time):
    if time < datetime.time(hour=8, minute=0, second=0) or time > datetime.time(hour=20, minute=0, second=0):
        raise ValidationError("reservation time should be between 8:00am to 8:00pm", params={name: time})


