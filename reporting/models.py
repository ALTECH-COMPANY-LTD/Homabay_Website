from django.db import models

class ProductionReport(models.Model):
    date = models.DateField()
    total_output = models.PositiveIntegerField()
    defect_rate = models.FloatField()