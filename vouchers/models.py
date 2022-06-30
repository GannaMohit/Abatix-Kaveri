from django.db import models
from masters.models import Customer, Metal, Purity, Category

# Create your models here.
class Voucher(models.Model):
    voucher_number = models.IntegerField()
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
        return f"{customer.name} {type} {date}"

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
        return f"{purity.purity} {metal.metal} {category.category}"
