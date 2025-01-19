from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

class Material(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock_level = models.PositiveIntegerField()