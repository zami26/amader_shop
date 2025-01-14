# Generated by Django 5.1.4 on 2024-12-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_wishlist_product_wishlist_products_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('La', 'Laptop'), ('Mo', 'Mobile'), ('Tab', 'Tablet'), ('TV', 'TV'), ('Ga', 'Gaming'), ('App', 'Appliance'), ('Ac', 'Accessories')], max_length=5),
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
