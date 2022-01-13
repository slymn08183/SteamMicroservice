from django.db import models


class Description(models.Model):
    # id = models.AutoField(primary_key=True)
    long = models.TextField(null=True, blank=True)
    short = models.TextField(null=True, blank=True)
