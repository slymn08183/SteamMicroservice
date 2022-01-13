import datetime
from django.db import models


class Price(models.Model):
    # id = models.AutoField(primary_key=True)
    discount = models.CharField(max_length=10, null=True, blank=True)
    original = models.CharField(max_length=10, null=True, blank=True)
    discount_fmt = models.CharField(max_length=15, null=True, blank=True)
    original_fmt = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
