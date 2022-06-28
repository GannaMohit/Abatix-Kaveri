from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=64)
    firm = models.CharField(max_length=64, blank=True)
    pan = models.CharField(max_length=64, blank=True)
    gst = models.CharField(max_length=64, blank=True)
    contact = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return name

class Total(models.Model):
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2)
    cgst = models.DecimalField(max_digits=16, decimal_places=2)
    igst = models.DecimalField(max_digits=16, decimal_places=2)
    tcs = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)

from sales.models import Advance

class Payment(models.Model):
    method_choices = [
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
        ("NEFT", "NEFT"),
        ("RTGS", "RTGS"),
        ("IMPS", "IMPS"),
        ("UPI", "UPI")
    ]
    method = models.CharField(max_length=16, choices=method_choices)
    amount = models.DecimalField(max_digits=16, max_digits=16, decimal_places=2)
    date = models.DateField()
    name = models.CharField(max_length=64)

    card_bank = models.CharField(max_length=64, blank=True)
    card_number = models.CharField(max_length=64, blank=True)

    cheque_number = models.CharField(max_length=64, blank=True)
    cheque_branch = models.CharField(max_length=64, blank=True)
    cheque_account_number = models.CharField(max_length=64, blank=True)
    cheque_ifsc = models.CharField(max_length=64, blank=True)

    upi_vpa = models.CharField(max_length=64, blank=True)
    upi_mobile = models.CharField(max_length=64, blank=True)

    wire_account_number = models.CharField(max_length=64, blank=True)
    wire_utr = models.CharField(max_length=64, blank=True)
    wire_bank = models.CharField(max_length=64, blank=True)

    advance = models.ForeignKey(Advance, on_delete=models.CASCADE, blank=True, related_name="payments")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, related_name="payments")

    def __str__(self):
        return f"{amount} {method}"
