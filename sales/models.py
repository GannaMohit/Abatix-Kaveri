from django.db import models
from masters.models import Customer, Total

# Create your models here.
class Advance(models.Model):
    date = models.DateField()
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="advance")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, related_name="advances")
    redeemed = models.BooleanField(default=False)

    def __str__(self):
        return f"{customer.name} ({date})"

class Home_Sale(models.Model):
    date = models.DateField()

    def __str__(self):
        return f"{date}"

class Invoice(models.Model):
    bill_number = models.IntegerField()
    date = models.DateField()
    gst_bill = models.CharField(max_length=64, unique=True)
    gst_state = models.CharField(max_length=64)
    tax = models.OneToOneField(Tax, on_delete=models.CASCADE, related_name="invoices")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    rates = models.JSONField()

    def __str__(self):
        return f"{customer.name} ({date})"

class Untagged(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="untagged")
    # TODO: Add metal, purity, category FK when tables are made
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3)
    less_weight = models.DecimalField(max_digits=16, decimal_places=3)
