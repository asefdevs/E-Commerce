# Generated by Django 4.2.5 on 2023-10-14 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0004_product_brand'),
        ('shopflow', '0004_alter_cart_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorites',
            name='products',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='shopflow.cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='estore.product'),
        ),
    ]