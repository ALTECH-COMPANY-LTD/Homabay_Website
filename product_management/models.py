from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    specifications = models.TextField()
    quantity_in_stock = models.PositiveIntegerField()