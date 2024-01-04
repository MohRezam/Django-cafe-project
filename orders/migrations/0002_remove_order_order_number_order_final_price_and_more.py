# Generated by Django 5.0 on 2024-01-04 19:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_number',
        ),
        migrations.AddField(
            model_name='order',
            name='final_price',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='کد تخفیف '),
        ),
        migrations.AlterField(
            model_name='order',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='table_number',
            field=models.IntegerField(verbose_name=' شماره میز '),
        ),
    ]
