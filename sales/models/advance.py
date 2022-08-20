from django.db import models
from masters.models import Customer, GST_State
from .invoice import Invoice
from django.urls import reverse

class Advance(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="advances")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True, related_name="advances")
    redeemed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.name} ({self.date})"

    def get_absolute_url(self):
        return reverse("advances")
