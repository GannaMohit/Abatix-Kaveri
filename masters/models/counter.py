from django.db import models

class Counter(models.Model):
    invoice_number = models.IntegerField()
    voucher_number = models.IntegerField()
