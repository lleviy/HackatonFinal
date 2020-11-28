from django.db import models

from accounts.models import User


class Region(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Space(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name + ' ' + self.owner.email


class ElectricityConsumption(models.Model):
    """Потребление электроэнергии"""
    year = models.CharField(max_length=4)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    consumption = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.region.name + ' ' + self.year + ' '
