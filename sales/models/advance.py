from django.db import models
from masters.models import Customer, GST_State
from .invoice import Invoice
from django.urls import reverse

class Advance(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="advances")
    redeemed = models.BooleanField(default=False)

    @property
    def amount(self):
        sum = self.payments.aggregate(models.Sum('amount', default=0, output_field=models.DecimalField()))["amount__sum"]
        return round(sum, 3)

    def __str__(self):
        return f"{self.customer.name}-{self.date}-{self.amount} "

    def get_absolute_url(self):
        return reverse("advances")
