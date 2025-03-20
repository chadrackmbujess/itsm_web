from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import LoginHistory
from django.utils import timezone

User = get_user_model()

@receiver(pre_delete, sender=User)
def log_user_logout(sender, instance, **kwargs):
    # Enregistrer la déconnexion
    session_log = LoginHistory.objects.filter(user=instance, logout_time__isnull=True).last()
    if session_log:
        session_log.logout_time = timezone.now()
        session_log.save()

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.timezone import now
from django.dispatch import receiver
from .models import CustomUser

def get_client_ip(request):
    """ Récupère l'adresse IP de l'utilisateur """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    """ Marquer l'utilisateur comme en ligne lors de la connexion """
    user.is_online = True
    user.last_login_time = now()
    user.last_ip = get_client_ip(request)
    user.save()

@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    """ Marquer l'utilisateur comme hors ligne à la déconnexion """
    user.is_online = False
    user.save()

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
