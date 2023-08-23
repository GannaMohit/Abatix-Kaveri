from django.db import models
from masters.models import Customer, Metal, Type, Purity, Category, GST_State
from stock.models import Product
import datetime

# Create your models here.

def get_voucher_number(type):
    today = datetime.date.today()
    last_april_date = datetime.date(today.year, 4, 1)
    if last_april_date > today:
        last_april_date = last_april_date.replace(year=today.year - 1)
    last_april_date_time = datetime.datetime.combine(last_april_date, datetime.time.min)
    return Voucher.objects.filter(date__gt = last_april_date_time, type=type).count() + 1

class Voucher(models.Model):
    voucher_number = models.IntegerField(verbose_name="Vch No.")
    type = models.CharField(max_length=16, choices=[
    ("Issue", "Issue"),
    ("Receive", "Receive"),
    ("URD", "URD")
    ])
    state = models.ForeignKey(GST_State, on_delete=models.CASCADE, related_name='voucher')
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
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name="particular")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="particular")
    purity = models.ForeignKey(Purity, on_delete=models.CASCADE, related_name="particular")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="particular")
    pieces = models.IntegerField(default=1)
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Gross Wt.")
    studs_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Studs Wt.")
    less_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Less Wt.")
    net_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Net Wt.")
    rate = models.DecimalField(max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="SGST")
    cgst = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="CGST")
    igst = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="IGST")
    tcs = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="TCS")
    total = models.DecimalField(max_digits=16, decimal_places=2)

class Voucher_Product(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name="products")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="voucher")
    rate = models.DecimalField(max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2)
    cgst = models.DecimalField(max_digits=16, decimal_places=2)
    igst = models.DecimalField(max_digits=16, decimal_places=2)
    tcs = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)
