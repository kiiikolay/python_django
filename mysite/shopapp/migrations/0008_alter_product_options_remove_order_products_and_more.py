# Generated by Django 5.1.2 on 2024-11-02 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price'], 'verbose_name_plural': 'prodects'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AlterModelTable(
            name='product',
            table='tech_products',
        ),
    ]
