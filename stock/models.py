from django.db import models
from masters.models import Metal, Purity, Type, Category, Stud_Type, Unit
from django.urls import reverse

import datetime

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=64)
    firm = models.CharField(max_length=64, blank=True)
    contact = models.CharField(max_length=16, blank=True)
    email = models.EmailField(blank=True)
    old_id = models.CharField(max_length=16, blank=True)
    old_description = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.name} {self.firm} ({self.old_id})"

class Product(models.Model):
    register_id = models.CharField(max_length=16,blank=True, null=True, verbose_name='Register')
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name="products")
    purity = models.ForeignKey(Purity, on_delete=models.CASCADE, related_name="products")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    pieces = models.IntegerField(default=1)
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Gross Wt.")
    studs_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Studs Wt.")
    less_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Less Wt.")
    net_weight = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="Net Wt.")

    rate = models.DecimalField(max_digits=16, decimal_places=2)
    calculation = models.CharField(max_length=32, blank=False, default="Making Charges", choices=[
    ("Making Charges", "Making Charges"),
    ("Wastage", "Wastage"),
    ("MRP", "MRP")
    ])
    making_charges = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True, verbose_name='Making')
    wastage = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    mrp = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True, verbose_name="MRP")

    description = models.TextField(blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")
    purchase_date = models.DateField(default=datetime.date.today, verbose_name="Date")
    lot_number = models.IntegerField(blank=True, null=True, verbose_name="Lot Number")
    design_code = models.CharField(max_length=32, blank=True, verbose_name='Design Code')
    old_id = models.CharField(max_length=16, blank=True, verbose_name='Jilaba ID')
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk} - {self.purity.purity} {self.metal.metal} {self.category.category}"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk' : self.pk})

class Stud(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="studs")
    type = models.ForeignKey(Stud_Type, on_delete=models.CASCADE, related_name="studs")
    less = models.BooleanField(default=False)
    colour = models.CharField(max_length=64, blank=True)
    shape = models.CharField(max_length=64, blank=True)
    quantity = models.IntegerField(default=1)
    weight = models.DecimalField(max_digits=16, decimal_places=3)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="studs")
    rate = models.DecimalField(max_digits=16, decimal_places=2)
    value = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return f"{self.type.type}"
