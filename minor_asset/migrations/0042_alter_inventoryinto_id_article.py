# Generated by Django 4.2.6 on 2023-10-30 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minor_asset', '0041_rename_i_article_inventoryinto_id_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryinto',
            name='id_article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='minor_asset.inventory'),
        ),
    ]
