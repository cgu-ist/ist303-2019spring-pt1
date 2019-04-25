from django.db import models
from django.db.models import (
    CharField,
    DecimalField,
    DateTimeField,
    PositiveIntegerField,
    BooleanField,
    EmailField,
    AutoField
)
from administration.validators import validate_int15_multipler


# Create your models here.
class Service(models.Model):
    id = AutoField
    name = CharField(max_length=255, unique=True)
    description = CharField(max_length=255)
    min_service_time = PositiveIntegerField(validators=[validate_int15_multipler])
    max_service_time = PositiveIntegerField(validators=[validate_int15_multipler])
    rate = DecimalField(blank=False, null=False, decimal_places=2, max_digits=5, validators=[DecimalField])
    limit = PositiveIntegerField(blank=False, null=False, default=65535)
    create_time = DateTimeField(auto_now_add=True)
    update_time = DateTimeField(auto_now=True)

    def __str__(self):
        return f"name: {self.name}\n description: {self.description}\n  min_service_time: {self.min_service_time} max_service_time: {self.max_service_time}\n rate: {self.rate} limit: {self.limit}"


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(active=True)


class Customer(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    UNKNOWN = 'Unknown'

    GENDER = ((MALE, 'male'), (FEMALE, 'female'), (UNKNOWN, 'unknown'))
    id = AutoField
    first_name = CharField(max_length=255)
    middle_name = CharField(max_length=255, null=True, blank=True)
    last_name = CharField(max_length=255)
    gender = CharField(max_length=7, choices=GENDER, default=UNKNOWN)
    active = BooleanField(default=True)
    tel = CharField(max_length=13, default=True)
    email = EmailField(null=True)
    check_in_time = DateTimeField(null=True)
    create_time = DateTimeField(auto_now_add=True)
    update_time = DateTimeField(auto_now=True)

    objects = models.Manager()
    actives = ActiveManager()

    def full_name(self):
        return self.first_name + " " + self.last_name;

    def __str__(self):
        return f"Customer id: {self.id}, name: {self.first_name} {self.last_name}, sex: {self.gender}, {self.active}"
