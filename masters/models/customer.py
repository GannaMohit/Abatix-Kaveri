from django.db import models
from masters.models.gst import GST_State

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=64)
    firm = models.CharField(max_length=64, blank=True)
    pan = models.CharField(max_length=64, blank=True)
    gst = models.CharField(max_length=64, blank=True)
    aadhar = models.CharField(max_length=64, blank=True)
    contact = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.ForeignKey(GST_State, on_delete=models.CASCADE, related_name='gst_state')
    country = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name
