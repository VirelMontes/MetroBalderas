# Generated by Django 4.2 on 2024-01-30 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_remove_cartitem_price_remove_product_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]