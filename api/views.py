from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import Profile, Event, Registration
from .serializers import RegisterSerializer, UserSerializer, EventSerializer, RegistrationSerializer


# Inscription
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# Profil utilisateur connecté
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Liste et création d'événements
class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Event.objects.all()
        return Event.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


# Détail, modification, suppression d'un événement
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Event.objects.all()
        return Event.objects.filter(is_public=True)


# S'inscrire à un événement
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_to_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Événement introuvable'}, status=404)

    if Registration.objects.filter(participant=request.user, event=event).exists():
        return Response({'error': 'Déjà inscrit à cet événement'}, status=400)

    Registration.objects.create(participant=request.user, event=event)
    return Response({'message': 'Inscription réussie'}, status=201)


# Mes inscriptions (participant)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_registrations(request):
    registrations = Registration.objects.filter(participant=request.user)
    serializer = RegistrationSerializer(registrations, many=True)
    return Response(serializer.data)


# Liste des participants d'un événement (organisateur)
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


# Dashboard organisateur
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard(request):
    events = Event.objects.filter(organizer=request.user)
    data = []
    for event in events:
        data.append({
            'id': event.id,
            'title': event.title,
            'date': event.date,
            'registrations_count': event.registrations.count(),
        })
    return Response(data)