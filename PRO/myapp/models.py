import uuid
from django.db import models


# Create your models here.
class Driver(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, default=None)
    years_of_experience = models.CharField(max_length=10)
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=False)


class Bus(models.Model):
    STATUS = [(0, "On platform"), (1, "Arriving"), (2, "Leaving"), (3, "Left")]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration_plate = models.CharField(max_length=30)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, default=None)
    end_destination = models.CharField(max_length=30)
    time_of_departure = models.TimeField(auto_now=False, auto_now_add=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    max_seats = models.IntegerField()
    seats_available = models.IntegerField()
    status = models.IntegerField(choices=STATUS)
