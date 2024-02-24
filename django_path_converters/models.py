from django.db import models

class Group(models.Model):
    level = models.IntegerField(unique=True)