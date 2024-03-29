# Generated by Django 4.2.7 on 2024-02-14 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minor_asset', '0053_inventory_weight_inventoryinto_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostics',
            name='cooling',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='diagnostics',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='diagnostics',
            name='engin_oil',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='diagnostics',
            name='fuel',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='diagnostics',
            name='grease',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='diagnostics',
            name='hydraulic_oil',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='diagnostics',
            name='time_decimal_hour',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='diagnostics',
            name='transmission_oil',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='inventoryinto',
            name='capacity',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='inventoryinto',
            name='price_unit',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True),
        ),
    ]
