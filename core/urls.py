from . import views
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet,TicketListCreateView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
#router.register(r'machines', MachineViewSet)
router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet)
router.register(r'maintenance-logs', MaintenanceLogViewSet)
router.register(r'equipment-history', EquipmentHistoryViewSet)
#router.register(r'tickets', TicketListCreateView)

urlpatterns = [
    #path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="user-list"),
    path('check-auth/', CheckAuthView.as_view(), name="check-auth"),
    path('login-history/', LoginHistoryView.as_view(), name='login-history'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('admin/session-logs/', session_logs, name='session_logs'),
    path('userss/', views.user_list, name='user_list'),
    path('userss/<int:user_id>/activity/', views.user_activity_history, name='user_activity_history'),
    path('ping/', PingView.as_view(), name='ping'),
    path('user_status/', UserStatusView.as_view(), name='user_status'),
    path('update_online_status/', UpdateOnlineStatusView.as_view(), name='update_online_status'),
    path('ping/manual/', ManualPingView.as_view(), name='manual-ping'),
    path('maintenance/schedule/', views.schedule_maintenance, name='schedule_maintenance'),
    path('maintenance/history/<int:equipment_id>/', views.maintenance_history, name='maintenance_history'),
    path('maintenance/alerts/', views.maintenance_alerts, name='maintenance_alerts'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/commentaires/', CommentaireListCreateView.as_view(), name='commentaire-list-create'),
    #path('tickets/<int:pk>/commentaires/', CommentaireListCreateView.as_view(), name='commentaire-list'),
    path('tickets/<int:pk>/pieces-jointes/', PieceJointeListCreateView.as_view(), name='piece-jointe-list'),
    #path('register-machine/', RegisterMachineView.as_view(), name="register-machine"),
    #path('installed-apps/', InstalledAppsView.as_view(), name='installed-apps'),
]
