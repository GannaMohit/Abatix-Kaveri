from .invoice import *
from .home_sale import *
from .advance import *
from django.db import models
# Create your models here.

class Invoice_Advance(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="advances")
    advance = models.ForeignKey(Advance, on_delete=models.CASCADE, related_name="invoice")

    def delete(self, *args, **kwargs):
        self.advance.redeemed = False
        self.advance.save()
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.advance.redeemed = True
        self.advance.save()
        super().save(*args, **kwargs)

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
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField()
    name = models.CharField(max_length=64, blank=True)

    card_bank = models.CharField(max_length=64, blank=True, verbose_name='Bank')
    card_number = models.CharField(max_length=64, blank=True, verbose_name="Card No.")

    cheque_number = models.CharField(max_length=64, blank=True, verbose_name="Cheque No.")
    cheque_branch = models.CharField(max_length=64, blank=True, verbose_name="Branch")
    cheque_account_number = models.CharField(max_length=64, blank=True, verbose_name="Account No.")
    cheque_ifsc = models.CharField(max_length=64, blank=True, verbose_name="IFSC")

    upi_vpa = models.CharField(max_length=64, blank=True, verbose_name="VPA")
    upi_mobile = models.CharField(max_length=64, blank=True, verbose_name="Mobile No.")

    wire_account_number = models.CharField(max_length=64, blank=True, verbose_name="Account No.")
    wire_utr = models.CharField(max_length=64, blank=True, verbose_name="UTR")
    wire_bank = models.CharField(max_length=64, blank=True, verbose_name="Bank")

    advance = models.ForeignKey(Advance, on_delete=models.CASCADE, blank=True, null=True, related_name="payments")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True, related_name="payments")

    def __str__(self):
        return f"{self.amount} {self.method}"
