# Generated by Django 4.2.5 on 2023-10-15 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopflow', '0008_alter_cartitem_cart_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
