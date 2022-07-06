# Generated by Django 4.0.5 on 2022-07-05 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=64, unique=True)),
                ('abbreviation', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.IntegerField()),
                ('voucher_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('firm', models.CharField(blank=True, max_length=64)),
                ('pan', models.CharField(blank=True, max_length=64)),
                ('gst', models.CharField(blank=True, max_length=64)),
                ('aadhar', models.CharField(blank=True, max_length=64)),
                ('contact', models.CharField(blank=True, max_length=64)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.TextField(blank=True)),
                ('pincode', models.CharField(blank=True, max_length=16)),
                ('city', models.CharField(blank=True, max_length=64)),
                ('state', models.CharField(blank=True, max_length=64)),
                ('country', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='GST_Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64, unique=True)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='GST_State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('state', models.CharField(max_length=64)),
                ('apha_code', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='HSN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=8)),
                ('igst', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Metal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal', models.CharField(max_length=32, unique=True)),
                ('symbol', models.CharField(blank=True, max_length=32)),
                ('colour', models.CharField(blank=True, max_length=32)),
                ('melting_point', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('boiling_point', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('density', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purity', models.DecimalField(decimal_places=2, max_digits=16, unique=True)),
                ('karatage', models.CharField(blank=True, max_length=32)),
                ('display_name', models.CharField(blank=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Stud_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64, unique=True)),
                ('latin_name', models.CharField(blank=True, max_length=64)),
                ('hindi_name', models.CharField(blank=True, max_length=64)),
                ('precious', models.BooleanField(default=False)),
                ('abbreviation', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=64, unique=True)),
                ('symbol', models.CharField(max_length=8)),
                ('value_gram', models.DecimalField(decimal_places=2, max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64, unique=True)),
                ('abbreviation', models.CharField(blank=True, max_length=16)),
                ('hsn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='masters.hsn')),
            ],
        ),
    ]
