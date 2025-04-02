from django.db import models
from people.models import *

class PurchaseRequirement(models.Model):
    material = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE)
    required_quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='purchase_requirements')

    def __str__(self):
        return f"{self.material.name} - {self.required_quantity}"

