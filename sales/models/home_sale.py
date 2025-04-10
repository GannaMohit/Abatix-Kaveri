from django.db import models
from stock.models import Product
from django.urls import reverse

import datetime

class Home_Sale(models.Model):
    date = models.DateField(default=datetime.date.today)

    @property
    def gross_weight(self):
        products_sum = self.products.aggregate(models.Sum('product__gross_weight', default=0, output_field=models.DecimalField()))["product__gross_weight__sum"]
        return round(products_sum, 3)

    @property
    def less_weight(self):
        products_sum = self.products.aggregate(models.Sum('product__less_weight', default=0, output_field=models.DecimalField()))["product__less_weight__sum"]
        return round(products_sum, 3)

    @property
    def net_weight(self):
        products_sum = self.products.aggregate(models.Sum('product__net_weight', default=0, output_field=models.DecimalField()))["product__net_weight__sum"]
        return round(products_sum, 3)

    def __str__(self):
        return f"{self.date}"

    def get_absolute_url(self):
        return reverse('home_sales')

class Home_Sale_Product(models.Model):
    home_sale = models.ForeignKey(Home_Sale, on_delete=models.CASCADE, related_name="products")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="home_sale")

    def delete(self, *args, **kwargs):
        self.product.sold = False
        self.product.save()
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.product.sold = True
        self.product.save()
        super().save(*args, **kwargs)
