from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Equipment, MaintenanceLog, EquipmentHistory
from core.models import LoginHistory

User = get_user_model()

# Serializer pour personnaliser le token JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

# Serializer pour l'enregistrement des utilisateurs
from rest_framework import serializers
from .models import CustomUser

from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password',
            'hostname', 'os_name', 'os_version', 'ip_address', 'mac_address',
            'cpu_info', 'cpu_freq', 'ram_info', 'wifi_cards', 'network_cards'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            hostname=validated_data['hostname'],
            os_name=validated_data['os_name'],
            os_version=validated_data['os_version'],
            ip_address=validated_data['ip_address'],
            mac_address=validated_data['mac_address'],
            cpu_info=validated_data['cpu_info'],
            cpu_freq=validated_data['cpu_freq'],
            ram_info=validated_data['ram_info'],
            wifi_cards=validated_data['wifi_cards'],
            network_cards=validated_data['network_cards'],
        )
        return user

from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    last_login_time = serializers.DateTimeField(source="last_login", format="%Y-%m-%d %H:%M:%S", read_only=True)
    last_ip = serializers.CharField(read_only=True)

    hostname = serializers.CharField(required=True)
    os_name = serializers.CharField(required=True)
    os_version = serializers.CharField(required=True)
    ip_address = serializers.CharField(required=True)
    mac_address = serializers.CharField(required=True)
    wifi_cards = serializers.IntegerField(required=True)
    network_cards = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_technician', 'is_admin',
            "last_login_time", "last_ip",
            "hostname", "os_name", "os_version", "ip_address", "mac_address",
            "wifi_cards", "network_cards"
        ]

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['user', 'ip_address', 'login_time']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'

class EquipmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentHistory
        fields = '__all__'

from rest_framework import serializers
from .models import Ticket, Commentaire, PieceJointe

class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Afficher le nom de l'utilisateur
    technicien = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )


    class Meta:
        model = Ticket
        fields = '__all__'

class CommentaireSerializer(serializers.ModelSerializer):
    auteur = serializers.ReadOnlyField(source='auteur.username')
    ticket_titre = serializers.ReadOnlyField(source='ticket.title')  # Ajoutez cette ligne

    class Meta:
        model = Commentaire
        fields = '__all__'

class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointe
        fields = '__all__'
