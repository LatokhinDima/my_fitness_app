from django.db import models
from django.contrib.auth.models import User


class SportsCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SportsFacility(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    picture = models.ImageField(upload_to='images/', default='')
    category = models.ManyToManyField(SportsCategory, related_name='sports_facilities')

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0)
    facility = models.ForeignKey(SportsFacility, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name
