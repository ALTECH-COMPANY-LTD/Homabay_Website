from django.db import models

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

class ProductionLine(models.Model):
    name = models.CharField(max_length=100)
    raw_materials = models.ManyToManyField(RawMaterial)
    schedule_time = models.DateTimeField()

class FinishedProduct(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)