from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Event, Registration


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['organizer', 'participant'], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, role=role)
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    registrations_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date',
                  'image', 'is_public', 'organizer', 'created_at', 'registrations_count']

    def get_registrations_count(self, obj):
        return obj.registrations.count()


class RegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    participant = UserSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'event', 'participant', 'registered_at']