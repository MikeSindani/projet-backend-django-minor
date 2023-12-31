# Generated by Django 4.1.7 on 2023-09-23 21:00

from django.db import migrations, models
import django.db.models.deletion
import minor_asset.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rue', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('ville', models.CharField(blank=True, max_length=50, null=True)),
                ('pays', models.CharField(blank=True, max_length=50, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='articles/')),
                ('nom', models.CharField(max_length=250)),
                ('prenom', models.CharField(max_length=250)),
                ('postnom', models.CharField(max_length=250)),
                ('matricule', models.CharField(max_length=10, unique=True)),
                ('phone1', models.CharField(max_length=10)),
                ('phone2', models.CharField(blank=True, max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('rue', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('quarter', models.CharField(blank=True, max_length=150, null=True)),
                ('commune', models.CharField(blank=True, max_length=150, null=True)),
                ('ville', models.CharField(blank=True, max_length=50, null=True)),
                ('pays', models.CharField(blank=True, max_length=50, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('isSupervisor', models.BooleanField(default=False)),
                ('isAssistant', models.BooleanField(default=False)),
                ('isAgent', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategorieMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriePanne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('date_modification', models.DateTimeField(auto_now=True, null=True)),
                ('time_modified', models.TimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CodePanne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_categorie_panne', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.categoriepanne')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(blank=True, max_length=250, null=True)),
                ('unit', models.CharField(blank=True, max_length=20, null=True)),
                ('capacity', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('currency', models.CharField(blank=True, max_length=20, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='articles/')),
                ('code_bar', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.categoryinventory')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='articles/')),
                ('nom', models.CharField(max_length=250)),
                ('marque', models.CharField(max_length=250)),
                ('modele', models.CharField(max_length=250)),
                ('annee_fabrique', models.IntegerField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.categoriemachine')),
            ],
        ),
        migrations.CreateModel(
            name='PlanifierMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(choices=[('haut', 'Haut'), ('normal', 'Normal'), ('basse', 'Basse')], max_length=10)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.machine')),
            ],
        ),
        migrations.CreateModel(
            name='PlanifierRepair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_taking_action', models.DateTimeField()),
                ('breakdown_description', models.CharField(max_length=200)),
                ('action', models.CharField(max_length=200)),
                ('target_running_date', models.DateTimeField()),
                ('priorite', models.CharField(blank=True, choices=[('haut', 'Haut'), ('normal', 'Normal'), ('basse', 'Basse')], max_length=10)),
                ('comments', models.TextField(blank=True, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.machine')),
            ],
        ),
        migrations.CreateModel(
            name='PlanifierTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone1', models.CharField(max_length=10)),
                ('phone2', models.CharField(blank=True, max_length=10)),
                ('web_site', models.CharField(blank=True, max_length=250)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('rue', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.IntegerField()),
                ('quarter', models.CharField(blank=True, max_length=150, null=True)),
                ('commune', models.CharField(blank=True, max_length=150, null=True)),
                ('ville', models.CharField(blank=True, max_length=50, null=True)),
                ('pays', models.CharField(blank=True, max_length=50, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('team_type', models.CharField(choices=[('MAINTENANCE', 'MAINTENANCE'), ('INVENTAIRE', 'INVENTAIRE'), ('OTHERS', 'OTHERS')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('work_order', models.CharField(default=minor_asset.models.generate_work_order, max_length=6, primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_code_panne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.codepanne')),
                ('id_inventaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.inventory')),
                ('id_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.machine')),
            ],
        ),
        migrations.CreateModel(
            name='Remind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_remind', models.DateTimeField(blank=True, null=True)),
                ('day', models.CharField(blank=True, max_length=1, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_planifierMaintenance', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.planifiermaintenance')),
                ('id_planifierRepair', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.planifierrepair')),
                ('id_planifierTeam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.planifierteam')),
            ],
        ),
        migrations.AddField(
            model_name='planifierteam',
            name='id_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.team'),
        ),
        migrations.CreateModel(
            name='InventoryOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_agent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.agent')),
                ('id_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.inventory')),
                ('id_team', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.team')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryInto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('userOrNew', models.CharField(blank=True, max_length=20, null=True)),
                ('unit', models.CharField(blank=True, max_length=20, null=True)),
                ('capacity', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('description', models.TextField(blank=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_article', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.inventory')),
            ],
        ),
        migrations.AddField(
            model_name='inventory',
            name='id_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.location'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='id_provider',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.provider'),
        ),
        migrations.CreateModel(
            name='Diagnostics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roster', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('typeMaintenance', models.CharField(max_length=100)),
                ('breakdown_date', models.DateField()),
                ('breakdown_time', models.TimeField()),
                ('start_repair_date', models.DateField()),
                ('start_repair_time', models.TimeField()),
                ('end_repair_date', models.DateField()),
                ('end_repair_time', models.TimeField()),
                ('priority', models.CharField(choices=[('haut', 'Haut'), ('normal', 'Normal'), ('basse', 'Basse')], max_length=10)),
                ('time_decimal_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('km_panne', models.IntegerField()),
                ('km_en_service', models.IntegerField()),
                ('fuel', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cooling', models.DecimalField(decimal_places=2, max_digits=10)),
                ('grease', models.DecimalField(decimal_places=2, max_digits=10)),
                ('engin_oil', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hydraulic_oil', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transmission_oil', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_diag_date', models.DateField()),
                ('start_diag_time', models.TimeField()),
                ('end_diag_time', models.TimeField()),
                ('end_diag_date', models.DateField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('id_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.machine')),
                ('id_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.team')),
                ('id_work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.workorder')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=250, null=True)),
                ('phone1', models.CharField(blank=True, max_length=10, null=True)),
                ('phone2', models.CharField(blank=True, max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('rue', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('quarter', models.CharField(blank=True, max_length=150, null=True)),
                ('commune', models.CharField(blank=True, max_length=150, null=True)),
                ('ville', models.CharField(blank=True, max_length=50, null=True)),
                ('pays', models.CharField(blank=True, max_length=50, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('time_modified', models.TimeField(auto_now=True)),
                ('asset_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minor_asset.machine')),
            ],
        ),
        migrations.AddField(
            model_name='categoryinventory',
            name='id_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minor_asset.location'),
        ),
    ]
