from django.db import models
from administration.models import Customer
from administration.models import Service
from django.db.models import (
    DateField,
    TimeField,
)
import datetime


# Create your models here.
class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = DateField()
    start_time = TimeField()
    end_time = TimeField()
    reservation_service = models.ForeignKey(Service, on_delete=models.CASCADE)

    objects = models.Manager()