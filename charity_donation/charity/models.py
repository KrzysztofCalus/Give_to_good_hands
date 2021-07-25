from django.db import models
from django.contrib.auth.models import User


# Create your models here.

TYPES = (
    ('fundacja', 'fundacja'),
    ('organizacja pozarządowa', 'organizacja pozarządowa'),
    ('zbiórka lokalna', 'zbiórka lokalna')
)


class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(choices=TYPES, default='fundacja', max_length=56)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)