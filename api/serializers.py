import random
import string
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event, Registration

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'password'   : { 'write_only': True },
            'first_name' : { 'required': False, 'default': 'Utilisateur' },
            'last_name'  : { 'required': False, 'default': '' },
            'role'       : { 'required': False, 'default': 'participant' },
        }

    def validate(self, data):
        # ← aucune validation bloquante
        return data

    def create(self, validated_data):
        # username unique auto-généré
        rand     = ''.join(random.choices(string.digits, k=6))
        username = (validated_data.get('email','user').split('@')[0])[:20] + rand

        user = User(
            username   = username,
            email      = validated_data.get('email', ''),
            first_name = validated_data.get('first_name', 'Utilisateur'),
            last_name  = validated_data.get('last_name', ''),
            role       = validated_data.get('role', 'participant'),
        )
        user.set_password(validated_data.get('password', '1234'))
        user.save()
        return user

class EventSerializer(serializers.ModelSerializer):
    organizer           = UserSerializer(read_only=True)
    registrations_count = serializers.SerializerMethodField()

    class Meta:
        model  = Event
        fields = '__all__'

    def get_registrations_count(self, obj):
        return obj.registrations.count()

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Event
        exclude = ['organizer']

class RegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model  = Registration
        fields = '__all__'