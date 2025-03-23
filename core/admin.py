from django.contrib import admin
from .models import (
    CustomUser, Equipment, MaintenanceLog, MaintenanceAlert,
    EquipmentHistory, UserActivity, Ticket, Commentaire, PieceJointe, LoginHistory
)

<<<<<<< HEAD
=======
# Filtre personnalisé pour is_online
>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
class IsOnlineFilter(admin.SimpleListFilter):
    title = 'En ligne'  # Titre du filtre
    parameter_name = 'is_online'  # Nom du paramètre dans l'URL

    def lookups(self, request, model_admin):
        # Définir les options du filtre
        return (
            ('true', 'En ligne'),
            ('false', 'Hors ligne'),
        )

    def queryset(self, request, queryset):
        # Appliquer le filtre
        if self.value() == 'true':
<<<<<<< HEAD
            # Utilisateurs avec une entrée LoginHistory is_online=True
            online_users = LoginHistory.objects.filter(is_online=True).values_list('user_id', flat=True)
            return queryset.filter(id__in=online_users)
        if self.value() == 'false':
            # Utilisateurs sans entrée LoginHistory is_online=True
            online_users = LoginHistory.objects.filter(is_online=True).values_list('user_id', flat=True)
            return queryset.exclude(id__in=online_users)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_technician', 'is_admin', 'get_is_online')
    search_fields = ('username', 'email')
    list_filter = ('is_technician', 'is_admin')
    readonly_fields = ('last_ip', 'last_login_time')

    def get_is_online(self, obj):
        """ Retourne l'état en ligne de l'utilisateur en fonction de LoginHistory """
        last_login_history = LoginHistory.objects.filter(user=obj).last()
        return last_login_history.is_online if last_login_history else False
    get_is_online.short_description = 'En ligne'
    get_is_online.boolean = True  # Affiche une icône vrai/faux dans l'admin

=======
            return queryset.filter(is_online=True)
        if self.value() == 'false':
            return queryset.filter(is_online=False)

# Configuration personnalisée pour CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_technician', 'is_admin', 'is_online')
    search_fields = ('username', 'email')
    list_filter = (IsOnlineFilter, 'is_technician', 'is_admin')  # Utilisez le filtre personnalisé
    readonly_fields = ('last_ip', 'last_login_time')  # Empêcher la modification manuelle
>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a

# Configuration personnalisée pour Equipment
class EquipmentStatusFilter(admin.SimpleListFilter):
    title = 'Statut de l\'équipement'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('new', 'Nouveau'),
            ('in_use', 'En utilisation'),
            ('under_maintenance', 'En maintenance'),
            ('retired', 'Retiré'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'status', 'assigned_to', 'location')
    search_fields = ('name', 'serial_number', 'assigned_to__username')
    list_filter = (EquipmentStatusFilter, 'location')
<<<<<<< HEAD
=======

>>>>>>> f1801716dfccfbab4437af9b6d089e6207084b3a
# Configuration personnalisée pour MaintenanceLog
@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'maintenance_date', 'performed_by', 'cost')
    search_fields = ('equipment__name', 'performed_by__username')
    list_filter = ('maintenance_date',)

# Configuration personnalisée pour MaintenanceAlert
@admin.register(MaintenanceAlert)
class MaintenanceAlertAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'alert_date', 'sent')
    search_fields = ('equipment__name',)
    list_filter = ('sent',)

# Configuration personnalisée pour EquipmentHistory
@admin.register(EquipmentHistory)
class EquipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'event_type', 'event_date', 'user')
    search_fields = ('equipment__name', 'user__username')
    list_filter = ('event_type',)

# Configuration personnalisée pour UserActivity
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type',)
    readonly_fields = ('timestamp',)  # Empêcher la modification manuelle

# Configuration personnalisée pour Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'categorie', 'statut', 'priorite', 'owner', 'technicien')
    search_fields = ('title', 'owner__username', 'technicien__username')
    list_filter = ('categorie', 'statut', 'priorite')

# Configuration personnalisée pour Commentaire
@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'auteur', 'date_creation')
    search_fields = ('ticket__title', 'auteur__username')
    readonly_fields = ('date_creation',)  # Empêcher la modification manuelle

# Configuration personnalisée pour PieceJointe
@admin.register(PieceJointe)
class PieceJointeAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'date_upload')
    search_fields = ('ticket__title',)
    readonly_fields = ('date_upload',)  # Empêcher la modification manuelle

# Configuration personnalisée pour LoginHistory
@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time', 'logout_time')
    list_filter = ('user', 'login_time')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('login_time', 'logout_time', 'ip_address')

    def has_add_permission(self, request):
        return False  # Empêcher l'ajout manuel de logs