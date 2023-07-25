from django.db import models
from masters.models import Customer, GST_State, Metal, Purity, Type, Category
from stock.models import Product
import datetime

def get_invoice_number():
    today = datetime.date.today()
    last_april_date = datetime.date(today.year, 4, 1)
    if last_april_date > today:
        last_april_date = last_april_date.replace(year=today.year - 1)
    return Invoice.objects.filter(date__gt = last_april_date).count() + 1

def get_gst_invoice():
    today = datetime.date.today()
    last_april_date = datetime.date(today.year, 4, 1)
    if last_april_date > today:
        last_april_date = last_april_date.replace(year=today.year - 1)
    invoice_number = Invoice.objects.filter(date__gt = last_april_date).count() + 1
    return f"{last_april_date.year}-{invoice_number}"

def get_gst_state():
    return GST_State.objects.get(state="Maharashtra")

class Invoice(models.Model):
    invoice_number = models.IntegerField(default=get_invoice_number, verbose_name='Inv. No.')
    date = models.DateField(default=datetime.date.today)
    gst_invoice = models.CharField(max_length=64, unique=True, default=get_gst_invoice)
    gst_state = models.ForeignKey(GST_State, on_delete=models.CASCADE, related_name="invoices", default=get_gst_state, verbose_name='state')

    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2)
    cgst = models.DecimalField(max_digits=16, decimal_places=2)
    igst = models.DecimalField(max_digits=16, decimal_places=2)
    tcs = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")

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
        return f"{self.customer.name} ({self.date})"

class Untagged(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="untagged")
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name="untagged")
    purity = models.ForeignKey(Purity, on_delete=models.CASCADE, related_name="untagged")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="untagged")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="untagged")
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

class Invoice_Product(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="products")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="invoice")
    rate = models.DecimalField(max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    sgst = models.DecimalField(max_digits=16, decimal_places=2)
    cgst = models.DecimalField(max_digits=16, decimal_places=2)
    igst = models.DecimalField(max_digits=16, decimal_places=2)
    tcs = models.DecimalField(max_digits=16, decimal_places=2)
    total = models.DecimalField(max_digits=16, decimal_places=2)
