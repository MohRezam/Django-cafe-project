# Generated by Django 5.0 on 2024-01-04 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_order_number_order_final_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table_number',
            field=models.IntegerField(null=True, verbose_name=' شماره میز '),
        ),
    ]
