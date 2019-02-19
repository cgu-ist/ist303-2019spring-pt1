from django.db import models
from administration.models import Customer
from administration.models import Service


# Create your models here.
class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reservation_date_time = models.DateTimeField
    reservation_service = models.ForeignKey(Service, on_delete=models.CASCADE)
