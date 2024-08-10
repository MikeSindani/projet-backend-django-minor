from django.db import models
from minor_asset.models import *
from users.models import *

# Create your models here.

class Setting(models.Model):
    weight = models.CharField(max_length=20,null=True, blank=True,default="Kilogram (kg)")
    currency = models.CharField(max_length=20,null=True, blank=True,default="CDF")
    capacity = models.CharField(max_length=20,null=True, blank=True,default="Litre (L)")
    distance = models.CharField(max_length=20,null=True, blank=True,default="Kilometer(km)")
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    entreprise = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.weight} -- {self.currency} -- {self.capacity}"