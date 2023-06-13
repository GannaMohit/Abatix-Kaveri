from django.db import models
from masters.models import Customer, Metal, Purity, Category
import datetime

# Create your models here.

def get_voucher_number():
    today = datetime.date.today()
    last_april_date = datetime.date(today.year, 4, 1)
    if last_april_date > today:
        last_april_date = last_april_date.replace(year=today.year - 1)
    last_april_date_time = datetime.datetime.combine(last_april_date, datetime.time.min)
    return Voucher.objects.filter(date__gt = last_april_date_time).count() + 1

class Voucher(models.Model):
    voucher_number = models.IntegerField(default=get_voucher_number)
    type = models.CharField(max_length=16, choices=[
    ("Issue", "Issue"),
    ("Receive", "Receive"),
    ("URD", "URD")
    ])
    date = models.DateField()
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3)
    net_weight = models.DecimalField(max_digits=16, decimal_places=3)
    pure_weight = models.DecimalField(max_digits=16, decimal_places=3)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="vouchers")

    def __str__(self):
        return f"{self.customer.name} {type} {self.date}"

class Particular(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name="particulars")
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name="particulars")
    purity = models.ForeignKey(Purity, on_delete=models.CASCADE, related_name="particulars")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="particulars")
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3)
    net_weight = models.DecimalField(max_digits=16, decimal_places=3)
    rate = models.DecimalField(max_digits=16, decimal_places=2)

    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2)
    cgst = models.DecimalField(max_digits=16, decimal_places=2)
    igst = models.DecimalField(max_digits=16, decimal_places=2)
    tcs = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return f"{self.purity.purity} {self.metal.metal} {self.category.category}"
