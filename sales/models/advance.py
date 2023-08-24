from django.db import models
from masters.models import Customer, GST_State
from .invoice import Invoice
from django.urls import reverse

import datetime

def get_advance_number():
    today = datetime.date.today()
    last_april_date = datetime.date(today.year, 4, 1)
    if last_april_date > today:
        last_april_date = last_april_date.replace(year=today.year - 1)
    return Advance.objects.filter(date__gt = last_april_date).count() + 1

def get_gst_state():
    return GST_State.objects.get(state="Maharashtra")

class Advance(models.Model):
    advance_number = models.IntegerField(default=get_advance_number, verbose_name='Adv. No.')
    date = models.DateField()
    state = models.ForeignKey(GST_State, on_delete=models.CASCADE, related_name='advances', default=get_gst_state)
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
