from django.db import models
from masters.models import Customer, GST_State, Metal, Purity, Type, Category
from stock.models import Product

def get_invoice_number():
    today = datetime.date.today()
    last_april_date = datetime.date(today.year, 4, 1)
    if last_april_date > today:
        last_april_date = last_april_date.replace(year=today.year - 1)
    last_april_date_time = datetime.combine(last_april_date, datetime.time.min)
    return Invoice.objects.filter(date__gt = last_april_date_time).count() + 1

class Invoice(models.Model):
    invoice_number = models.IntegerField(default=get_invoice_number)
    date = models.DateField()
    gst_invoice = models.CharField(max_length=64, unique=True)
    gst_state = models.ForeignKey(GST_State, on_delete=models.CASCADE, related_name="invoices")

    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2)
    cgst = models.DecimalField(max_digits=16, decimal_places=2)
    igst = models.DecimalField(max_digits=16, decimal_places=2)
    tcs = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    rates = models.JSONField()

    @property
    def gross_weight(self):
        products_sum = self.products.aggregate(models.Sum('product__gross_weight', default=0, output_field=models.DecimalField()))["product__gross_weight__sum"]
        untagged_sum = self.untagged.aggregate(models.Sum('gross_weight', default=0, output_field=models.DecimalField()))["gross_weight__sum"]
        return round(products_sum + untagged_sum, 3)

    @property
    def net_weight(self):
        products_sum = self.products.aggregate(models.Sum('product__net_weight', default=0, output_field=models.DecimalField()))["product__net_weight__sum"]
        untagged_sum = self.untagged.aggregate(models.Sum('net_weight', default=0, output_field=models.DecimalField()))["net_weight__sum"]
        return round(products_sum + untagged_sum, 3)

    def __str__(self):
        return f"{customer.name} ({date})"

class Untagged(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="untagged")
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name="untagged")
    purity = models.ForeignKey(Purity, on_delete=models.CASCADE, related_name="untagged")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="untagged")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="untagged")
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3)
    less_weight = models.DecimalField(max_digits=16, decimal_places=3)
    net_weight = models.DecimalField(max_digits=16, decimal_places=3)

class Invoice_Product(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="products")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="invoice")
