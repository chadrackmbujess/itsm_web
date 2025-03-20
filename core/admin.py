from django.contrib import admin
from .models import *

# Enregistrer les modèles
admin.site.register(CustomUser)
admin.site.register(Equipment)
admin.site.register(MaintenanceLog)
admin.site.register(MaintenanceAlert)
admin.site.register(EquipmentHistory)
admin.site.register(UserActivity)
admin.site.register(Ticket)
admin.site.register(Commentaire)
admin.site.register(PieceJointe)


# Configuration personnalisée pour LoginHistory
@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time', 'logout_time')
    list_filter = ('user', 'login_time')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('login_time', 'logout_time', 'ip_address')

    def has_add_permission(self, request):
        return False  # Empêcher l'ajout manuel de logs