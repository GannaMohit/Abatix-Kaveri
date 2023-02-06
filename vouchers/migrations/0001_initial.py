# Generated by Django 4.1.2 on 2023-02-04 13:28

from django.db import migrations, models
import django.db.models.deletion
import vouchers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_number', models.IntegerField(default=vouchers.models.get_voucher_number)),
                ('type', models.CharField(choices=[('Issue', 'Issue'), ('Receive', 'Receive'), ('URD', 'URD')], max_length=16)),
                ('date', models.DateField()),
                ('gross_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('net_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('pure_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='masters.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Particular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gross_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('net_weight', models.DecimalField(decimal_places=3, max_digits=16)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=16)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=16)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('igst', models.DecimalField(decimal_places=2, max_digits=16)),
                ('tcs', models.DecimalField(decimal_places=2, max_digits=16)),
                ('total', models.DecimalField(decimal_places=2, max_digits=16)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='masters.category')),
                ('metal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='masters.metal')),
                ('purity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='masters.purity')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='particulars', to='vouchers.voucher')),
            ],
        ),
    ]
