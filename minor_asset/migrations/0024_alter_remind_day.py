# Generated by Django 4.1.7 on 2023-10-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minor_asset', '0023_remove_remind_id_planifierrepair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remind',
            name='day',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
