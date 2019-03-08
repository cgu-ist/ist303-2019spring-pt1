from django.db import models
from administration.models import Customer
from administration.models import Service
from django.db.models import (
    IntegerField,
    DateTimeField
)
import datetime


# Create your models here.
class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reservation_date_time = DateTimeField()
    reservation_length = IntegerField()
    reservation_service = models.ForeignKey(Service, on_delete=models.CASCADE)

    objects = models.Manager()