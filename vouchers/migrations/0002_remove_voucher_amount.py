# Generated by Django 4.1.2 on 2023-08-28 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voucher',
            name='amount',
        ),
    ]
