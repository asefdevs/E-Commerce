# Generated by Django 4.2.5 on 2023-10-16 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflow', '0012_order_products_alter_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]