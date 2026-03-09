from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response

from .models import Event, Registration
from .serializers import EventSerializer, RegisterSerializer, RegistrationSerializer, UserSerializer


class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.organizer == request.user


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Event.objects.filter(Q(is_public=True) | Q(organizer=user))
        return Event.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Event.objects.filter(Q(is_public=True) | Q(organizer=user))
        return Event.objects.filter(is_public=True)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_to_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Événement introuvable'}, status=404)

    if not event.is_public and event.organizer != request.user:
        return Response({'error': 'Accès refusé'}, status=403)

    if Registration.objects.filter(participant=request.user, event=event).exists():
        return Response({'error': 'Déjà inscrit à cet événement'}, status=400)

    Registration.objects.create(participant=request.user, event=event)
    return Response({'message': 'Inscription réussie'}, status=201)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_registrations(request):
    registrations = Registration.objects.filter(participant=request.user)
    serializer = RegistrationSerializer(registrations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def event_participants(request, event_id):
    try:
        event = Event.objects.get(id=event_id, organizer=request.user)
    except Event.DoesNotExist:
        return Response({'error': 'Événement introuvable ou accès refusé'}, status=404)

    registrations = Registration.objects.filter(event=event)
    serializer = RegistrationSerializer(registrations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard(request):
    events = Event.objects.filter(organizer=request.user)
    data = []
    for event in events:
        data.append(
            {
                'id': event.id,
                'title': event.title,
                'date': event.date,
                'registrations_count': event.registrations.count(),
            }
        )
    return Response(data)
