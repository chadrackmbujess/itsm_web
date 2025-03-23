# Generated by Django 5.1.5 on 2025-03-23 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_customuser_is_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='status',
            field=models.CharField(choices=[('Nouveau', 'Nouveau'), ('En_utilisation', 'En utilisation'), ('En_maintenance', 'En maintenance'), ('Retiré', 'Retiré')], default='new', max_length=50, verbose_name='Statut'),
        ),
    ]
