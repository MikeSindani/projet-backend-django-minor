from django.db import models

# Create your models here.

class Setting(models.Model):
    weight = models.CharField(max_length=20,null=True, blank=True)
    currency = models.CharField(max_length=20,null=True, blank=True)
    capacity = models.CharField(max_length=20,null=True, blank=True)
    distance = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.weight} -- {self.currency} -- {self.capacity}"