# Generated by Django 5.2.1 on 2025-05-22 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_order_options_order_status'),
        ('production', '0002_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.product'),
        ),
    ]
