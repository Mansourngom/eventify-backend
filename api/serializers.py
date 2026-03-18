from django.contrib.auth import get_user_model
from rest_framework import serializers
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
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        import random, string
        username = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        user = User.objects.create_user(
            username   = username,
            email      = validated_data.get('email', ''),
            password   = validated_data.get('password', ''),
            first_name = validated_data.get('first_name', ''),
            last_name  = validated_data.get('last_name', ''),
            role       = validated_data.get('role', 'participant'),
        )
        return user

class EventSerializer(serializers.ModelSerializer):
    organizer_name      = serializers.SerializerMethodField()
    registrations_count = serializers.SerializerMethodField()

    class Meta:
        model  = Event
        fields = '__all__'
        extra_kwargs = {'organizer': {'read_only': True}}

    def get_organizer_name(self, obj):
        return f"{obj.organizer.first_name} {obj.organizer.last_name}"

    def get_registrations_count(self, obj):
        return obj.registrations.count()

class RegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user  = UserSerializer(read_only=True)

    class Meta:
        model  = Registration
        fields = '__all__'