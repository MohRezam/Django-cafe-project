# Generated by Django 5.0 on 2023-12-30 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0006_alter_item_image_alter_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255, verbose_name='محصول'),
        ),
    ]