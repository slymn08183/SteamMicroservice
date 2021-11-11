from django.db import models


class Description(models.Model):
    # id = models.AutoField(primary_key=True)
    long = models.TextField()
    short = models.TextField()
