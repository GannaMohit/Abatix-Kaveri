from django.db import models
from masters.models import Customer, GST_State

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
    gst_state = models.ForeignKey(GST_State, on_delete=models.CASCADE, related_name="invoices")

    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2)
    cgst = models.DecimalField(max_digits=16, decimal_places=2)
    igst = models.DecimalField(max_digits=16, decimal_places=2)
    tcs = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    rates = models.JSONField()

    def __str__(self):
        return f"{customer.name} ({date})"

class Untagged(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="untagged")
    metal = models.ForeignKey(Metal, on_delete=CASCADE, related_name="products")
    purity = models.ForeignKey(Purity, on_delete=CASCADE, related_name="products")
    # TODO: Confirm if type is to be included or not
    type = models.ForeignKey(Type, on_delete=CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="products")
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3)
    less_weight = models.DecimalField(max_digits=16, decimal_places=3)
    net_weight = models.DecimalField(max_digits=16, decimal_places=3)

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
