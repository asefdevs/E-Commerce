# Generated by Django 4.2.5 on 2023-10-08 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0003_remove_product_brand_delete_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]