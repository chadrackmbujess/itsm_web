from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import LoginHistory
from django.utils import timezone

User = get_user_model()

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from .models import LoginHistory

User = get_user_model()

def get_client_ip(request):
    """ Récupère l'adresse IP de l'utilisateur """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def handle_user_login(sender, request, user, **kwargs):
    """ Gère la connexion de l'utilisateur """
    ip_address = get_client_ip(request)
    LoginHistory.objects.create(
        user=user,
        login_time=timezone.now(),
        ip_address=ip_address,
        is_online=True
    )

@receiver(user_logged_out)
def handle_user_logout(sender, request, user, **kwargs):
    """ Gère la déconnexion de l'utilisateur """
    session_log = LoginHistory.objects.filter(user=user, logout_time__isnull=True).last()
    if session_log:
        session_log.logout_time = timezone.now()
        session_log.is_online = False
        session_log.save()

@receiver(pre_delete, sender=User)
def log_user_logout_on_delete(sender, instance, **kwargs):
    """ Gère la déconnexion forcée lors de la suppression de l'utilisateur """
    session_log = LoginHistory.objects.filter(user=instance, logout_time__isnull=True).last()
    if session_log:
        session_log.logout_time = timezone.now()
        session_log.is_online = False
        session_log.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket

@receiver(post_save, sender=Ticket)
def envoyer_notification_ticket(sender, instance, created, **kwargs):
    if not created:  # Si le ticket est mis à jour
        send_mail(
            subject=f"Mise à jour du ticket: {instance.title,instance.description}",
            message=f"Le ticket '{instance.title}' a été mis à jour.\nCatégorie: {instance.categorie} \nNouveau statut: {instance.statut}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.owner.email],
            fail_silently=True,
        )
