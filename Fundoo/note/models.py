from django.db import models


class Contacts(models.Model):
    Name = models.CharField(max_length=22)
    MobileNumber = models.CharField(max_length=2200)
    Address = models.CharField(max_length=24)
