# Generated by Django 4.2.5 on 2023-10-08 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0002_alter_product_brand_alter_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
