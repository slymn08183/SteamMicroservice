from django.db import models


class Feature(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.TextField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

