# Generated by Django 4.2.7 on 2024-03-27 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minor_asset', '0061_alter_trackingpieces_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trackingpieces',
            old_name='quantity',
            new_name='quantity_total',
        ),
        migrations.AddField(
            model_name='trackingpieces',
            name='quantity_used',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
