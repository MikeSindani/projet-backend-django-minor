# Generated by Django 4.1.7 on 2023-10-08 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_team_agent_user_agent'),
        ('minor_asset', '0007_agent_created_by_agent_user_inventoryinto_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostics',
            name='id_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.team'),
        ),
        migrations.AlterField(
            model_name='inventoryout',
            name='id_agent',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.agent'),
        ),
        migrations.AlterField(
            model_name='inventoryout',
            name='id_team',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.team'),
        ),
        migrations.AlterField(
            model_name='planifierteam',
            name='id_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.team'),
        ),
        migrations.DeleteModel(
            name='Agent',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
