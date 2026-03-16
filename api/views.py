<<<<<<< Updated upstream
from rest_framework import generics, permissions, status
from rest_framework.response import Response
=======
>>>>>>> Stashed changes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from .models import Event, Registration
from .serializers import (
    UserSerializer, RegisterSerializer,
    EventSerializer, EventCreateSerializer,
    RegistrationSerializer
)

User = get_user_model()

<<<<<<< Updated upstream
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

=======
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access' : str(refresh.access_token),
        'user'   : UserSerializer(user).data,
    }
>>>>>>> Stashed changes

# S'inscrire à un événement
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(get_tokens(user), status=201)
    # Si erreur on essaie quand même de créer
    data = request.data
    import random, string
    rand     = ''.join(random.choices(string.digits, k=8))
    username = 'user_' + rand
    user     = User(
        username   = username,
        email      = data.get('email', ''),
        first_name = data.get('first_name', 'Utilisateur'),
        last_name  = data.get('last_name', ''),
        role       = data.get('role', 'participant'),
    )
    user.set_password(data.get('password', '1234'))
    user.save()
    return Response(get_tokens(user), status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email    = request.data.get('email', '').strip()
    password = request.data.get('password', '').strip()
    user     = None

    # Cherche par email
    user_qs = User.objects.filter(email=email)
    for u in user_qs:
        result = authenticate(request, username=u.username, password=password)
        if result:
            user = result
            break

    if user:
        return Response(get_tokens(user))
    return Response({'error': 'Identifiants incorrects'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def event_list(request):
    events   = Event.objects.all().order_by('-created_at')
    search   = request.query_params.get('search', '')
    category = request.query_params.get('category', '')
    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    if category:
        events = events.filter(category=category)
    return Response(EventSerializer(events, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error': 'Événement introuvable'}, status=404)
    return Response(EventSerializer(event).data)

<<<<<<< Updated upstream
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
=======
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_create(request):
    serializer = EventCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(organizer=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def event_update(request, pk):
>>>>>>> Stashed changes
    try:
        event = Event.objects.get(pk=pk, organizer=request.user)
    except Event.DoesNotExist:
        return Response({'error': 'Introuvable'}, status=404)
    serializer = EventCreateSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def event_delete(request, pk):
    try:
        event = Event.objects.get(pk=pk, organizer=request.user)
    except Event.DoesNotExist:
        return Response({'error': 'Introuvable'}, status=404)
    event.delete()
    return Response({'message': 'Supprimé'}, status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_register(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error': 'Événement introuvable'}, status=404)
    if event.registrations.count() >= event.capacity:
        return Response({'error': 'Événement complet'}, status=400)
    if Registration.objects.filter(user=request.user, event=event).exists():
        return Response({'error': 'Déjà inscrit'}, status=400)
    reg = Registration.objects.create(user=request.user, event=event)
    return Response(RegistrationSerializer(reg).data, status=201)

# Dashboard organisateur
@api_view(['GET'])
<<<<<<< Updated upstream
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
=======
@permission_classes([IsAuthenticated])
def my_registrations(request):
    regs = Registration.objects.filter(
        user=request.user
    ).select_related('event').order_by('-created_at')
    return Response(RegistrationSerializer(regs, many=True).data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_registration(request, pk):
    try:
        reg = Registration.objects.get(pk=pk, user=request.user)
    except Registration.DoesNotExist:
        return Response({'error': 'Inscription introuvable'}, status=404)
    reg.delete()
    return Response({'message': 'Annulée'}, status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    events         = Event.objects.filter(organizer=request.user)
    total_inscrits = sum(e.registrations.count() for e in events)
    return Response({
        'total_events'  : events.count(),
        'total_inscrits': total_inscrits,
        'events'        : EventSerializer(events, many=True).data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_participants(request, pk):
    try:
        event = Event.objects.get(pk=pk, organizer=request.user)
    except Event.DoesNotExist:
        return Response({'error': 'Introuvable'}, status=404)
    regs = Registration.objects.filter(event=event).select_related('user')
    return Response(RegistrationSerializer(regs, many=True).data)
>>>>>>> Stashed changes
