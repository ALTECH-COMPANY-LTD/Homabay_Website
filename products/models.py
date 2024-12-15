from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('concrete_blocks', 'Concrete Blocks: Hollow blocks for versatile construction.'),
        ('drainage_solutions', 'Drainage Solutions: Invert blocks, shallow drains, road kerbs, channels, etc.'),
        ('landscaping_products', 'Landscaping Products: Paving slabs, side slabs, quadrants, and wall copings.'),
        ('manhole_components', 'Manhole Components: Rings, covers, cover slabs, and tapers.'),
        ('custom_pavers', 'Custom Pavers: Decorative and functional paving options.'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    dimensions = models.CharField(max_length=100)
    features = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)  
    image = models.ImageField(upload_to='products/')  

    def __str__(self):
        return self.name