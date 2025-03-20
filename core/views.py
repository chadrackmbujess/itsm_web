from sys import platform

from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import viewsets, permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate
from django.utils.timezone import now
import socket
from django.utils import timezone
from .models import CustomUser, LoginHistory, Equipment, MaintenanceLog, EquipmentHistory
from .serializers import CustomTokenObtainPairSerializer, LoginHistorySerializer, RegisterSerializer, UserSerializer, EquipmentSerializer, MaintenanceLogSerializer, EquipmentHistorySerializer
from .permissions import IsAdminOrReadOnly
from django.utils.timezone import localtime


User = get_user_model()

# Fonction pour vérifier l'expiration du token
def check_token_expiration(token):
    """
    Vérifie si un token JWT est expiré.
    Retourne True si le token est valide, False s'il est expiré ou invalide.
    """
    try:
        access_token = AccessToken(token)
        access_token.verify()  # Vérifie si le token est valide (non expiré et correctement signé)
        return True
    except TokenError as e:
        print(f"Erreur de token : {e}")
        return False

# Vue pour obtenir le token JWT
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        installed_apps = request.data.get('installed_apps', [])  # Récupérer les applications installées

        user = authenticate(username=username, password=password)

        if user is not None:
            client_ip = request.META.get('REMOTE_ADDR') or socket.gethostbyname(socket.gethostname())

            # Enregistrer la connexion dans l'historique
            LoginHistory.objects.create(user=user, ip_address=client_ip, is_online=True)

            # Vérifier si l'IP a changé
            if user.last_ip != client_ip:
                # Envoyer une alerte par e-mail
                subject = "🔐 Alerte de Connexion - Nouvelle IP"
                message = (
                    f"Bonjour {user.username},\n\n"
                    f"Nous avons détecté une connexion depuis une nouvelle adresse IP : {client_ip}.\n"
                    f"Si ce n'était pas vous, veuillez modifier votre mot de passe immédiatement.\n\n"
                    f"Cordialement,\nL'équipe de sécurité."
                )
                send_mail(
                    subject,
                    message,
                    'chadrackmbujess@gmail.com',  # Remplace par ton adresse
                    [user.email],
                    fail_silently=False
                )

            # Enregistrer la connexion dans l'historique
            LoginHistory.objects.create(user=user, ip_address=client_ip)

            # Mettre à jour les informations de l'utilisateur
            user.last_ip = client_ip
            user.last_login = now()
            user.installed_apps = installed_apps  # Stocker les applications installées
            user.save()

            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "last_ip": user.last_ip,
                "last_login_time": user.last_login,
                "installed_apps": user.installed_apps  # Retourner les applications installées
            })

        return Response({"error": "Identifiants invalides"}, status=401)

# Vue pour afficher l'historique des connexions
class LoginHistoryView(generics.ListAPIView):
    queryset = LoginHistory.objects.all()
    serializer_class = LoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Vue pour enregistrer un nouvel utilisateur
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

# Vue pour gérer les utilisateurs
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Vérifier si le token est expiré
        token = request.auth
        if not check_token_expiration(token):
            return Response({"error": "Token expiré ou invalide"}, status=status.HTTP_401_UNAUTHORIZED)

        print("Requête reçue par UserViewSet")
        return super().list(request, *args, **kwargs)

# Vue pour lister les utilisateurs
class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Vérifier si le token est expiré
        token = request.auth
        if not check_token_expiration(token):
            return Response({"error": "Token expiré ou invalide"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().list(request, *args, **kwargs)

# Vue pour vérifier l'authentification
class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Vérifier si le token est expiré
        token = request.auth
        if not check_token_expiration(token):
            return Response({"error": "Token expiré ou invalide"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Vous êtes authentifié !"})

# Vue pour gérer la déconnexion
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Récupérer le refresh token
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Le refresh token est requis"}, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si le token est un refresh token valide
            try:
                token = RefreshToken(refresh_token)
            except TokenError as e:
                return Response({"error": "Token invalide ou déjà expiré"}, status=status.HTTP_400_BAD_REQUEST)

            # Mettre à jour l'heure de déconnexion dans LoginHistory
            user = request.user
            session_log = LoginHistory.objects.filter(user=user, logout_time__isnull=True).last()
            if session_log:
                session_log.logout_time = timezone.now()
                session_log.is_online = False  # Mettre à jour l'état en ligne
                session_log.save()

            # Ajouter le token à la liste noire
            token.blacklist()

            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vue pour gérer les équipements
class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Vérifier si le token est expiré
        token = request.auth
        if not check_token_expiration(token):
            return Response({"error": "Token expiré ou invalide"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().list(request, *args, **kwargs)

# Vue pour gérer les logs de maintenance
class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Vérifier si le token est expiré
        token = request.auth
        if not check_token_expiration(token):
            return Response({"error": "Token expiré ou invalide"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().list(request, *args, **kwargs)

# Vue pour gérer l'historique des équipements
class EquipmentHistoryViewSet(viewsets.ModelViewSet):
    queryset = EquipmentHistory.objects.all()
    serializer_class = EquipmentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Vérifier si le token est expiré
        token = request.auth
        if not check_token_expiration(token):
            return Response({"error": "Token expiré ou invalide"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().list(request, *args, **kwargs)

# Vue pour afficher les logs de session dans l'admin
def session_logs(request):
    logs = LoginHistory.objects.all()
    return render(request, 'admin/session_logs.html', {'logs': logs})

from django.shortcuts import render
from django.db.models import Max
from .models import User, LoginHistory
import subprocess
from django.shortcuts import render
from django.db.models import Max
from .models import User, LoginHistory

def ping(host):
    """
    Ping une machine pour vérifier si elle est en ligne.
    Retourne True si la machine répond, False sinon.
    """
    try:
        # Utiliser la commande ping (Windows ou Linux)
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except Exception as e:
        print(f"Erreur lors du ping : {e}")
        return False

from datetime import timedelta

def user_list(request):
    users = User.objects.annotate(
        #last_login=Max('login_history__login_time'),
        last_activity=Max('login_history__logout_time')
    ).order_by('-last_login')

    inactivity_threshold = timedelta(minutes=5)  # Définir le seuil d'inactivité

    for user in users:
        user.is_online = ping(user.last_ip)
        user.is_inactive = (now() - user.last_activity) > inactivity_threshold if user.last_activity else False

    return render(request, 'admin/user_list.html', {'users': users})

from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import User, LoginHistory

def user_activity_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    date_filter = request.GET.get('date_filter')

    # Filtrer les activités par date si une date est fournie
    activities = user.login_history.all().order_by('-login_time')
    if date_filter:
        activities = activities.filter(
            Q(login_time__date=date_filter) | Q(logout_time__date=date_filter)
    )

    return render(request, 'admin/user_activity_history.html', {
        'user': user,
        'activities': activities,
        'date_filter': date_filter
    })

from django.http import JsonResponse
from django.views import View

class PingView(View):
    def get(self, request):
        ip = request.GET.get('ip')
        if not ip:
            return JsonResponse({'success': False, 'error': 'Adresse IP manquante'})

        is_online = ping(ip)
        return JsonResponse({'success': is_online})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateOnlineStatusView(APIView):
    def post(self, request):
        username = request.data.get("username")
        is_online = request.data.get("is_online")

        if not username or is_online is None:
            return Response({"error": "Données manquantes"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            # Mettre à jour l'état en ligne dans LoginHistory
            session_log = LoginHistory.objects.filter(user=user, logout_time__isnull=True).last()
            if session_log:
                session_log.is_online = is_online
                session_log.save()
            return Response({"message": "État en ligne mis à jour"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import LoginHistory
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

class UserStatusView(APIView):
    def get(self, request):
        users = User.objects.annotate(
            last_activity=Max('login_history__logout_time')
        ).order_by('-last_login')

        inactivity_threshold = timedelta(minutes=5)  # Définir le seuil d'inactivité

        user_status = []
        for user in users:
            user_status.append({
                "id": user.id,
                "username": user.username,
                "is_online": user.login_history.filter(is_online=True).exists(),
                "last_activity": user.last_activity,
            })

        return Response({"users": user_status}, status=status.HTTP_200_OK)

from django.http import JsonResponse
from django.views import View
from .utils import ping  # Importez votre fonction ping
from django.contrib.auth import get_user_model

User = get_user_model()

class ManualPingView(View):
    def get(self, request):
        ip_or_username = request.GET.get('target')  # Récupérer l'IP ou le nom d'utilisateur depuis la requête

        if not ip_or_username:
            return JsonResponse({'success': False, 'error': 'Veuillez spécifier une IP ou un nom d\'utilisateur.'}, status=400)

        # Si c'est un nom d'utilisateur, récupérer l'IP associée
        if not ip_or_username.replace('.', '').isdigit():  # Vérifier si c'est une IP ou un nom d'utilisateur
            try:
                user = User.objects.get(username=ip_or_username)
                ip_or_username = user.last_ip  # Utiliser l'IP de l'utilisateur
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé.'}, status=404)

        # Effectuer le ping
        is_online = ping(ip_or_username)
        return JsonResponse({'success': True, 'is_online': is_online, 'target': ip_or_username})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Equipment, MaintenanceLog
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Equipment, MaintenanceLog

def maintenance_history(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    maintenance_logs = MaintenanceLog.objects.filter(equipment=equipment).order_by('-maintenance_date')
    logs_data = [
        {
            "date": log.maintenance_date.strftime("%Y-%m-%d"),
            "description": log.description,
            "performed_by": log.performed_by.username if log.performed_by else "N/A",
            "cost": str(log.cost) if log.cost else "N/A",
        }
        for log in maintenance_logs
    ]
    return JsonResponse({"success": True, "logs": logs_data})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Equipment, MaintenanceLog
from .forms import MaintenanceForm

def schedule_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Maintenance planifiée avec succès."})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)

from django.http import JsonResponse
from .models import MaintenanceAlert

def maintenance_alerts(request):
    alerts = MaintenanceAlert.objects.filter(sent=False).order_by('-alert_date')
    alerts_data = [
        {
            "equipment": alert.equipment.name,
            "alert_date": alert.alert_date.strftime("%Y-%m-%d"),
            "message": alert.message,
        }
        for alert in alerts
    ]
    return JsonResponse({"success": True, "alerts": alerts_data})

from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Equipment

User = get_user_model()

def admin_dashboard(request):
    users = User.objects.all()
    equipments = Equipment.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'users': users, 'equipments': equipments})

from rest_framework import generics, permissions
from .models import Ticket, Commentaire, PieceJointe
from .serializers import TicketSerializer, CommentaireSerializer, PieceJointeSerializer

class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import generics, permissions
from .models import Commentaire, PieceJointe
from .serializers import CommentaireSerializer, PieceJointeSerializer

class CommentaireListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtrer les commentaires par l'utilisateur connecté
        return Commentaire.objects.filter(auteur=self.request.user)

    def perform_create(self, serializer):
        # Associer l'utilisateur connecté au commentaire lors de la création
        serializer.save(auteur=self.request.user)

class PieceJointeListCreateView(generics.ListCreateAPIView):
    serializer_class = PieceJointeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtrer les pièces jointes par l'utilisateur connecté
        return PieceJointe.objects.filter(auteur=self.request.user)

    def perform_create(self, serializer):
        # Associer l'utilisateur connecté à la pièce jointe lors de la création
        serializer.save(auteur=self.request.user)