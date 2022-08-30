from django.db import models


class Trip(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    place = models.CharField(max_length=50)
    country = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'trips_trip'