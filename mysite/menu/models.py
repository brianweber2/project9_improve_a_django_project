from django.db import models
from django.utils import timezone


# def convert_utc_to_pst(utc_time):
#     """Converts UTC time to PST time."""
#     from mysite.settings import TIME_ZONE
#     import pytz
#     tz = pytz.timezone(TIME_ZONE)
#     pst_time = utc_time.astimezone(tz)
#     return pst_time


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.season

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(
            default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        'Ingredient', related_name='ingredients'
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
