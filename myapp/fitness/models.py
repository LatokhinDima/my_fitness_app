from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


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


class OrderEntry(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="+")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_entries")

    def __str__(self):
        return f'{self.service} - {self.start_date} - {self.end_date}'


class Status(models.TextChoices):
    INITIAL = 'INITIAL', 'Initial'
    COMPLETED = 'COMPLETED', 'Completed'
    DELIVERED = 'DELIVERED', 'Delivered'


class Order(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIAL)

    def __str__(self):
        return f'{self.profile} - {self.status}'

    def get_total_price(self):
        return sum(order_entry.service.price for order_entry in self.order_entries.all())

    def get_order_status(self):
        if self.status == Status.INITIAL:
            return 'INITIAL'
        elif self.status == Status.COMPLETED:
            return 'COMPLETED'
        elif self.status == Status.DELIVERED:
            return 'DELIVERED'
        else:
            return 'UNKNOWN'

    def calculate_end_date(self):
        start_dates = [entry.start_date for entry in self.order_entries.all()]
        end_dates = []
        for start_date in start_dates:
            end_date = start_date + timedelta(days=30)
            end_dates.append(end_date)
        return end_dates


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    shopping_cart = models.OneToOneField(Order, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='shopping_cart')

    def __str__(self):
        return str(self.user)
