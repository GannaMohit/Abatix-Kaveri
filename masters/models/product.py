from django.db import models
from .gst import HSN

class Metal(models.Model):
    metal = models.CharField(max_length=32, unique=True)
    symbol = models.CharField(max_length=32, blank=True)
    colour = models.CharField(max_length=32, blank=True)
    melting_point = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    boiling_point = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    density = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.metal

class Purity(models.Model):
    purity = models.DecimalField(max_digits=16, decimal_places=2, unique=True)
    karatage = models.CharField(max_length=32, blank=True)
    display_name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"{self.purity}"

class Type(models.Model):
    type = models.CharField(max_length=64, unique=True)
    hsn = models.ForeignKey(HSN, on_delete=models.CASCADE, related_name="types")
    abbreviation = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.type

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    abbreviation = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.category

class Stud_Type(models.Model):
    type = models.CharField(max_length=64, unique=True)
    latin_name = models.CharField(max_length=64, blank=True)
    hindi_name = models.CharField(max_length=64, blank=True)
    precious = models.BooleanField(default=False)
    abbreviation = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.type

class Unit(models.Model):
    unit = models.CharField(max_length=64, unique=True)
    symbol = models.CharField(max_length=8)
    value_gram = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return self.symbol
