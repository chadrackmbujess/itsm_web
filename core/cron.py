from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import Equipment, MaintenanceLog, MaintenanceAlert

class ScheduleMaintenanceCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Exécuter tous les jours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.schedule_maintenance_cron_job'

    def do(self):
        today = timezone.now().date()
        equipments = Equipment.objects.filter(next_maintenance_date__lte=today)

        for equipment in equipments:
            # Enregistrer la maintenance
            MaintenanceLog.objects.create(
                equipment=equipment,
                maintenance_date=today,
                description="Maintenance préventive planifiée."
            )

            # Planifier la prochaine maintenance
            equipment.last_maintenance_date = today
            equipment.schedule_next_maintenance()
            equipment.save()

            # Créer une alerte pour les utilisateurs
            alert_date = today - timezone.timedelta(days=7)  # Alerte 7 jours avant
            MaintenanceAlert.objects.create(
                equipment=equipment,
                alert_date=alert_date,
                message=f"Maintenance préventive prévue pour {equipment.name} le {today}."
            )

from django.core.mail import send_mail
from django.conf import settings
from .models import MaintenanceAlert
from django.utils import timezone

class SendMaintenanceAlertsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Exécuter tous les jours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.send_maintenance_alerts_cron_job'

    def do(self):
        today = timezone.now().date()
        alerts = MaintenanceAlert.objects.filter(alert_date=today, sent=False)

        for alert in alerts:
            if alert.equipment.assigned_to:
                send_mail(
                    subject=f"Alerte de Maintenance : {alert.equipment.name}",
                    message=alert.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[alert.equipment.assigned_to.email],
                    fail_silently=False,
                )

                # Marquer l'alerte comme envoyée
                alert.sent = True
                alert.save()