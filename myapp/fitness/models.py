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
    category = models.ForeignKey(SportsCategory, on_delete=models.CASCADE, related_name='sports_facilities')

    def __str__(self):
        return self.name


