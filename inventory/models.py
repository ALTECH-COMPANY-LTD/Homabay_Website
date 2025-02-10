from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import CustomUser  # Import your CustomUser model

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    quantity_available = models.FloatField()
    reorder_level = models.FloatField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def update_stock(self, quantity):
        """Updates the stock level of the raw material."""
        self.quantity_available += quantity
        self.save()

class Stock(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
    ]
    
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.FloatField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date']

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    tax_number = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('partially_received', 'Partially Received'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    expected_delivery = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO-{self.po_number} from {self.supplier.name} (Status: {self.status})"

    def save(self, *args, **kwargs):
        if not self.po_number:
            last_po = PurchaseOrder.objects.order_by('-id').first()
            if last_po:
                last_number = int(last_po.po_number.split('-')[-1])
                self.po_number = f"PO-{str(last_number + 1).zfill(5)}"
            else:
                self.po_number = "PO-00001"
        super().save(*args, **kwargs)

    def update_status(self):
        """Updates the status of the purchase order based on received quantities."""
        if all(item.received_quantity >= item.quantity for item in self.items.all()):
            self.status = 'completed'
        elif any(item.received_quantity > 0 for item in self.items.all()):
            self.status = 'partially_received'
        else:
            self.status = 'draft'
        self.save()

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.FloatField(default=0)

    @property
    def total_price(self):
        # Convert quantity to Decimal to avoid type errors during multiplication
        return Decimal(self.quantity) * self.unit_price

    def __str__(self):
        return f"{self.material.name} - {self.quantity} @ {self.unit_price}"

class MaterialReceiving(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    receiving_number = models.CharField(max_length=50, unique=True)
    receiving_date = models.DateTimeField(default=timezone.now)
    received_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Use CustomUser here
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receiving_number:
            last_receive = MaterialReceiving.objects.order_by('-id').first()
            if last_receive:
                last_number = int(last_receive.receiving_number.split('-')[-1])
                self.receiving_number = f"RCV-{str(last_number + 1).zfill(5)}"
            else:
                self.receiving_number = "RCV-00001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receiving {self.receiving_number} for {self.purchase_order.po_number}"

class MaterialReceivingItem(models.Model):
    receiving = models.ForeignKey(MaterialReceiving, related_name='items', on_delete=models.CASCADE)
    purchase_order_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.CASCADE)
    received_quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    notes = models.TextField(blank=True)

    def clean(self):
        # Ensure that received quantity does not exceed the ordered quantity
        if self.received_quantity > self.purchase_order_item.quantity - self.purchase_order_item.received_quantity:
            raise ValidationError("Received quantity cannot exceed the remaining quantity.")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean to validate before saving
        # Update the received quantity in the related PurchaseOrderItem
        self.purchase_order_item.received_quantity += self.received_quantity
        self.purchase_order_item.save()

        # Update stock
        self.purchase_order_item.material.update_stock(self.received_quantity)

        # Update the purchase order status
        self.purchase_order_item.purchase_order.update_status()

        super().save(*args, **kwargs)