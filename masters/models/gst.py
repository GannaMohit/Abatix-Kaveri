from django.db import models

class GST_State(models.Model):
    class Meta:
        verbose_name = "GST State"
        verbose_name_plural = "GST States"

    code = models.IntegerField()
    state = models.CharField(max_length=64)
    apha_code = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.code} - {self.state}"

class GST_Rate(models.Model):
    class Meta:
        verbose_name = "GST Rate"
        verbose_name_plural = "GST Rates"

    type = models.CharField(max_length=64, unique=True)
    percentage = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.type}: {self.percentage}%"

class HSN(models.Model):
    class Meta:
        verbose_name = "HSN"
        verbose_name_plural = "HSNs"

    code = models.IntegerField()
    sgst = models.DecimalField(max_digits=8, decimal_places=2)
    cgst = models.DecimalField(max_digits=8, decimal_places=2)
    igst = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code}"
