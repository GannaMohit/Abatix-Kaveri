# Generated by Django 4.1.2 on 2023-06-19 14:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
import sales.models.invoice


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0001_initial'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('redeemed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advances', to='masters.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Home_Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.IntegerField(default=sales.models.invoice.get_invoice_number)),
                ('date', models.DateField(default=datetime.date.today)),
                ('gst_invoice', models.CharField(default=sales.models.invoice.get_gst_invoice, max_length=64, unique=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=16)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('igst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('tcs', models.DecimalField(decimal_places=2, max_digits=16)),
                ('total', models.DecimalField(decimal_places=2, max_digits=16)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='masters.customer')),
                ('gst_state', models.ForeignKey(default=sales.models.invoice.get_gst_state, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='masters.gst_state')),
            ],
        ),
        migrations.CreateModel(
            name='Untagged',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gross_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('less_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('net_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=16)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=16)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('igst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('tcs', models.DecimalField(decimal_places=2, max_digits=16)),
                ('total', models.DecimalField(decimal_places=2, max_digits=16)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='untagged', to='masters.category')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='untagged', to='sales.invoice')),
                ('metal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='untagged', to='masters.metal')),
                ('purity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='untagged', to='masters.purity')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='untagged', to='masters.type')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('Cash', 'Cash'), ('Cheque', 'Cheque'), ('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('NEFT', 'NEFT'), ('RTGS', 'RTGS'), ('IMPS', 'IMPS'), ('UPI', 'UPI')], max_length=16)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=64)),
                ('card_bank', models.CharField(blank=True, max_length=64)),
                ('card_number', models.CharField(blank=True, max_length=64)),
                ('cheque_number', models.CharField(blank=True, max_length=64)),
                ('cheque_branch', models.CharField(blank=True, max_length=64)),
                ('cheque_account_number', models.CharField(blank=True, max_length=64)),
                ('cheque_ifsc', models.CharField(blank=True, max_length=64)),
                ('upi_vpa', models.CharField(blank=True, max_length=64)),
                ('upi_mobile', models.CharField(blank=True, max_length=64)),
                ('wire_account_number', models.CharField(blank=True, max_length=64)),
                ('wire_utr', models.CharField(blank=True, max_length=64)),
                ('wire_bank', models.CharField(blank=True, max_length=64)),
                ('advance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='sales.advance')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='sales.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=16)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=16)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('igst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('tcs', models.DecimalField(decimal_places=2, max_digits=16)),
                ('total', models.DecimalField(decimal_places=2, max_digits=16)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='sales.invoice')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='stock.product')),
            ],
        ),
        migrations.CreateModel(
            name='Home_Sale_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='sales.home_sale')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='home_sale', to='stock.product')),
            ],
        ),
        migrations.AddField(
            model_name='advance',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advances', to='sales.invoice'),
        ),
    ]
