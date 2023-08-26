# Generated by Django 4.1.2 on 2023-08-25 14:06

from django.db import migrations, models
import django.db.models.deletion
import vouchers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0001_initial'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_number', models.IntegerField(verbose_name='Vch No.')),
                ('type', models.CharField(choices=[('Issue', 'Issue'), ('Receive', 'Receive'), ('URD', 'URD')], max_length=16)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='masters.customer')),
                ('state', models.ForeignKey(default=vouchers.models.get_gst_state, on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='masters.gst_state')),
            ],
        ),
        migrations.CreateModel(
            name='Voucher_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=16)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=16)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('igst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('tcs', models.DecimalField(decimal_places=2, max_digits=16)),
                ('total', models.DecimalField(decimal_places=2, max_digits=16)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='voucher', to='stock.product')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='vouchers.voucher')),
            ],
        ),
        migrations.CreateModel(
            name='Particular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pieces', models.IntegerField(default=1)),
                ('gross_weight', models.DecimalField(decimal_places=3, max_digits=16, verbose_name='Gross Wt.')),
                ('studs_weight', models.DecimalField(decimal_places=3, max_digits=16, verbose_name='Studs Wt.')),
                ('less_weight', models.DecimalField(decimal_places=3, max_digits=16, verbose_name='Less Wt.')),
                ('net_weight', models.DecimalField(decimal_places=3, max_digits=16, verbose_name='Net Wt.')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=16)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=16)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='SGST')),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='CGST')),
                ('igst', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='IGST')),
                ('tcs', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='TCS')),
                ('total', models.DecimalField(decimal_places=2, max_digits=16)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='masters.category')),
                ('metal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='masters.metal')),
                ('purity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='masters.purity')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='masters.type')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='vouchers.voucher')),
            ],
        ),
    ]
