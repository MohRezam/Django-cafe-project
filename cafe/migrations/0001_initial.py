# Generated by Django 5.0 on 2024-01-07 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام')),
                ('logo_image', models.ImageField(upload_to='cafe/%Y', verbose_name='تصویر لوگو')),
                ('about_page_image', models.ImageField(upload_to='cafe/%Y', verbose_name='تصویر صفحه توضیحات')),
                ('about_page_description', models.TextField(verbose_name='توضیحات')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تماس')),
            ],
            options={
                'verbose_name_plural': 'کافه',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, unique=True, verbose_name='دسته بندی')),
                ('image', models.ImageField(upload_to='categories/%Y/%m/%d/', verbose_name='تصویر')),
            ],
            options={
                'verbose_name_plural': 'دسته بندی محصولات',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True, verbose_name='شماره میز')),
                ('is_available', models.BooleanField(default=True, verbose_name='موجود')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='محصول')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('image', models.ImageField(upload_to='items/%Y/%m/%d/', verbose_name='تصویر')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('ingredients', models.TextField(verbose_name='محتویات')),
                ('item_status', models.BooleanField(default=True, verbose_name='موجود')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.category', to_field='category_name', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name_plural': 'محصولات',
            },
        ),
    ]
