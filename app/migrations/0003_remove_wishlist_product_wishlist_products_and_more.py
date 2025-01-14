# Generated by Django 5.1.4 on 2024-12-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='products',
            field=models.ManyToManyField(to='app.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Ho', 'Hoodies'), ('La', 'Laptop'), ('Sh', 'Shoes'), ('Wa', 'Watches'), ('El', 'Electronics'), ('Su', 'Sunglasses'), ('Ts', 'T Shirts')], max_length=5),
        ),
    ]
