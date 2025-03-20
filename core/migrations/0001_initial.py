# Generated by Django 5.1.5 on 2025-03-11 04:52

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_technician', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('last_login_time', models.DateTimeField(blank=True, null=True)),
                ('hostname', models.CharField(blank=True, max_length=255, null=True)),
                ('os_name', models.CharField(blank=True, max_length=100, null=True)),
                ('os_version', models.CharField(blank=True, max_length=100, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('mac_address', models.CharField(blank=True, max_length=50, null=True)),
                ('cpu_info', models.CharField(blank=True, max_length=255, null=True)),
                ('cpu_freq', models.FloatField(blank=True, null=True)),
                ('ram_info', models.FloatField(blank=True, null=True)),
                ('wifi_cards', models.IntegerField(default=0)),
                ('network_cards', models.IntegerField(default=0)),
                ('is_online', models.BooleanField(default=False)),
                ('installed_apps', models.JSONField(blank=True, default=dict)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_users', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name="Nom de l'équipement")),
                ('serial_number', models.CharField(max_length=100, unique=True, verbose_name='Numéro de série')),
                ('manufacturer', models.CharField(max_length=100, verbose_name='Fabricant')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('purchase_date', models.DateField(verbose_name="Date d'achat")),
                ('warranty_end_date', models.DateField(verbose_name='Fin de garantie')),
                ('status', models.CharField(choices=[('new', 'Nouveau'), ('in_use', 'En utilisation'), ('under_maintenance', 'En maintenance'), ('retired', 'Retiré')], default='new', max_length=50, verbose_name='Statut')),
                ('location', models.CharField(max_length=255, verbose_name='Emplacement')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('last_maintenance_date', models.DateField(blank=True, null=True, verbose_name='Date de la dernière maintenance')),
                ('next_maintenance_date', models.DateField(blank=True, null=True, verbose_name='Date de la prochaine maintenance')),
                ('maintenance_interval_months', models.IntegerField(default=6, verbose_name='Intervalle de maintenance (mois)')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Assigné à')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField(auto_now_add=True, verbose_name="Date de l'événement")),
                ('event_type', models.CharField(choices=[('assignment', 'Assignation'), ('maintenance', 'Maintenance'), ('status_change', 'Changement de statut'), ('retirement', 'Mise hors service')], max_length=50, verbose_name="Type d'événement")),
                ('description', models.TextField(verbose_name="Description de l'événement")),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='core.equipment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur concerné')),
            ],
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(auto_now_add=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='login_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_date', models.DateField(verbose_name="Date de l'alerte")),
                ('message', models.TextField(verbose_name="Message de l'alerte")),
                ('sent', models.BooleanField(default=False, verbose_name='Alerte envoyée')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_alerts', to='core.equipment')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_date', models.DateField(verbose_name='Date de maintenance')),
                ('description', models.TextField(verbose_name='Description de la maintenance')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Coût')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_logs', to='core.equipment')),
                ('performed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Effectué par')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('categorie', models.CharField(choices=[('matériel', 'Problème matériel'), ('réseau', 'Problème réseau'), ('logiciel', 'Problème logiciel'), ('sécurité', 'Problème de sécurité')], default='logiciel', max_length=50)),
                ('statut', models.CharField(choices=[('ouvert', 'Ouvert'), ('en_cours', 'En cours'), ('résolu', 'Résolu'), ('fermé', 'Fermé')], default='ouvert', max_length=50)),
                ('priorite', models.CharField(choices=[('faible', 'Faible'), ('normal', 'Normal'), ('élevé', 'Élevé'), ('urgent', 'Urgent')], default='normal', max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('technicien', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets_assignes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PieceJointe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='pieces_jointes/')),
                ('date_upload', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pieces_jointes', to='core.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='core.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
