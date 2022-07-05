from django.db import models
from masters.models import Metal, Purity, Type, Category, Stud_Type, Unit
from sales.models import Invoice, Home_Sale

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=64)
    firm = models.CharField(max_length=64, blank=True)
    contact = models.CharField(max_length=16, blank=True)
    email = models.EmailField(blank=True)
    old_id = models.CharField(max_length=16, blank=True)
    old_description = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return name

class Product(models.Model):
    register_id = models.IntegerField(blank=True, null=True)
    metal = models.ForeignKey(Metal, on_delete=models.CASCADE, related_name="products")
    purity = models.ForeignKey(Purity, on_delete=models.CASCADE, related_name="products")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    pieces = models.IntegerField(default=1)
    gross_weight = models.DecimalField(max_digits=16, decimal_places=3)
    studs_weight = models.DecimalField(max_digits=16, decimal_places=3)
    less_weight = models.DecimalField(max_digits=16, decimal_places=3)
    net_weight = models.DecimalField(max_digits=16, decimal_places=3)

    calculation = models.CharField(max_length=32, choices=[
    ("Making_Charges", "Making_Charges"),
    ("Wastage", "Wastage"),
    ("MRP", "MRP")
    ])
    making_charges = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    wastage = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    mrp = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)

    description = models.TextField(blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")
    purchase_date = models.DateField(blank=True)
    lot_number = models.IntegerField(blank=True, null=True)
    design_code = models.CharField(max_length=32, blank=True)
    old_id = models.CharField(max_length=16, blank=True)

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    home_sale = models.ForeignKey(Home_Sale, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{purity.purity} {metal.metal} {category.category}"

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
        return f"{type.type}"
