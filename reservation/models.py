from django.db import models
from administration.models import Customer
from administration.models import Service
from django.db.models import (
    AutoField,
    DateField,
    TimeField,
)
from reservation.validators import (validate_start_time, validate_end_time)


# Create your models here.
class Reservation(models.Model):
    id = AutoField
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = DateField()
    start_time = TimeField(validators=[validate_start_time])
    end_time = TimeField(validators=[validate_end_time])
    reservation_service = models.ForeignKey(Service, on_delete=models.CASCADE)

    objects = models.Manager()


