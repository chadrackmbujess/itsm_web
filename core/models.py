from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_technician = models.BooleanField(default=False)  # Rôle technicien
    is_admin = models.BooleanField(default=False)  # Rôle admin
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_users", blank=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)

    # 🖥️ Infos de la machine
    hostname = models.CharField(max_length=255, null=True, blank=True)
    os_name = models.CharField(max_length=100, null=True, blank=True)
    os_version = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=50, null=True, blank=True)
    cpu_info = models.CharField(max_length=255, null=True, blank=True)  # Nom du CPU
    cpu_freq = models.FloatField(null=True, blank=True)  # Fréquence en GHz
    ram_info = models.FloatField(null=True, blank=True)  # RAM en Go
    wifi_cards = models.IntegerField(default=0)  # Nombre de cartes Wi-Fi
    network_cards = models.IntegerField(default=0)  # Nombre de cartes réseau
    #is_online = models.BooleanField(default=False)  # ✅ Indique si l'utilisateur est en ligne

    # 📌 Applications installées (stockées sous forme de JSON)

    installed_apps = models.JSONField(default=dict, blank=True)


    def save(self, *args, **kwargs):
        if not self.username.startswith("@"):
            self.username = f"@{self.username}.jessmi.cd"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

User = get_user_model()

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_online = models.BooleanField(default=False)  # Nouveau champ pour l'état en ligne

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - Connexion : {self.login_time}, Déconnexion : {self.logout_time}"

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)  # Exemple : "Connexion", "Déconnexion", "Modification de profil"
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"


User = get_user_model()

class Equipment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de l'équipement")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Numéro de série")
    manufacturer = models.CharField(max_length=100, verbose_name="Fabricant")
    model = models.CharField(max_length=100, verbose_name="Modèle")
    purchase_date = models.DateField(verbose_name="Date d'achat")
    warranty_end_date = models.DateField(verbose_name="Fin de garantie")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Assigné à")
    status = models.CharField(
        max_length=50,
        choices=[
            ('Nouveau', 'Nouveau'),
            ('En_utilisation', 'En utilisation'),
            ('En_maintenance', 'En maintenance'),
            ('Retiré', 'Retiré'),
        ],
        default='new',
        verbose_name="Statut"
    )
    location = models.CharField(max_length=255, verbose_name="Emplacement")
    notes = models.TextField(blank=True, verbose_name="Notes")
    last_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Date de la dernière maintenance")
    next_maintenance_date = models.DateField(blank=True, null=True, verbose_name="Date de la prochaine maintenance")
    maintenance_interval_months = models.IntegerField(default=6, verbose_name="Intervalle de maintenance (mois)")

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    def schedule_next_maintenance(self):
        if self.last_maintenance_date:
            self.next_maintenance_date = self.last_maintenance_date + timezone.timedelta(days=30 * self.maintenance_interval_months)
        else:
            self.next_maintenance_date = timezone.now().date() + timezone.timedelta(days=30 * self.maintenance_interval_months)
        self.save()

class MaintenanceLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="maintenance_logs")
    maintenance_date = models.DateField(verbose_name="Date de maintenance")
    description = models.TextField(verbose_name="Description de la maintenance")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Effectué par")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Coût")

    def __str__(self):
        return f"Maintenance de {self.equipment.name} le {self.maintenance_date}"

class MaintenanceAlert(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="maintenance_alerts")
    alert_date = models.DateField(verbose_name="Date de l'alerte")
    message = models.TextField(verbose_name="Message de l'alerte")
    sent = models.BooleanField(default=False, verbose_name="Alerte envoyée")

    def __str__(self):
        return f"Alerte pour {self.equipment.name} le {self.alert_date}"

class EquipmentHistory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="history")
    event_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'événement")
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('assignment', 'Assignation'),
            ('maintenance', 'Maintenance'),
            ('status_change', 'Changement de statut'),
            ('retirement', 'Mise hors service'),
        ],
        verbose_name="Type d'événement"
    )
    description = models.TextField(verbose_name="Description de l'événement")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilisateur concerné")

    def __str__(self):
        return f"{self.event_type} pour {self.equipment.name} le {self.event_date}"


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    CATEGORIES = [
        ('matériel', 'Problème matériel'),
        ('réseau', 'Problème réseau'),
        ('logiciel', 'Problème logiciel'),
        ('sécurité', 'Problème de sécurité'),
    ]

    STATUTS = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours'),
        ('résolu', 'Résolu'),
        ('fermé', 'Fermé'),
    ]

    PRIORITES = [
        ('faible', 'Faible'),
        ('normal', 'Normal'),
        ('élevé', 'Élevé'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='logiciel')
    statut = models.CharField(max_length=50, choices=STATUTS, default='ouvert')
    priorite = models.CharField(max_length=50, choices=PRIORITES, default='normal')
    date_creation = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    technicien = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assignes')

    def __str__(self):
        return f"Envoyé par {self.owner.username} | {self.title} |  Statut [{self.statut}] | Priorité [{self.priorite}] "

class Commentaire(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire sur {self.ticket.title} par {self.auteur.username}"

class PieceJointe(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='pieces_jointes')
    fichier = models.FileField(upload_to='pieces_jointes/')
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pièce jointe pour {self.ticket.title}"