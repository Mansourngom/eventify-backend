import uuid
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event, Registration
from .serializers import UserSerializer, EventSerializer, RegistrationSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data     = request.data
    username = 'user_' + uuid.uuid4().hex[:8]
    try:
        user = User.objects.create_user(
            username   = username,
            email      = data.get('email', ''),
            password   = data.get('password', ''),
            first_name = data.get('first_name', ''),
            last_name  = data.get('last_name', ''),
            role       = data.get('role', 'participant'),
        )
    except Exception as e:
        return Response({'detail': str(e)}, status=400)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access':  str(refresh.access_token),
        'refresh': str(refresh),
        'user':    UserSerializer(user).data,
    }, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email    = request.data.get('email', '')
    password = request.data.get('password', '')
    user_obj = User.objects.filter(email=email).first()
    if not user_obj:
        return Response({'detail': 'Identifiants incorrects'}, status=400)
    user = authenticate(request, username=user_obj.username, password=password)
    if not user:
        return Response({'detail': 'Identifiants incorrects'}, status=400)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access':  str(refresh.access_token),
        'refresh': str(refresh),
        'user':    UserSerializer(user).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def event_list(request):
    q        = request.query_params.get('q', '')
    category = request.query_params.get('category', '')
    events   = Event.objects.filter(is_private=False)
    if q:
        events = events.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        events = events.filter(category=category)
    return Response(EventSerializer(events.order_by('-created_at'), many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'detail': 'Introuvable'}, status=404)
    return Response(EventSerializer(event).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_create(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(organizer=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def event_update(request, pk):
    try:
        event = Event.objects.get(pk=pk, organizer=request.user)
    except Event.DoesNotExist:
        return Response({'detail': 'Introuvable'}, status=404)
    serializer = EventSerializer(event, data=request.data, partial=True)
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
        return Response({'detail': 'Introuvable'}, status=404)
    event.delete()
    return Response(status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_register(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'detail': 'Introuvable'}, status=404)
    if Registration.objects.filter(user=request.user, event=event).exists():
        return Response({'detail': 'Déjà inscrit'}, status=400)
    Registration.objects.create(user=request.user, event=event)
    return Response({'detail': 'Inscription réussie'}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_registrations(request):
    regs = Registration.objects.filter(user=request.user).select_related('event')
    return Response(RegistrationSerializer(regs, many=True).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_registration(request, pk):
    try:
        reg = Registration.objects.get(pk=pk, user=request.user)
    except Registration.DoesNotExist:
        return Response({'detail': 'Introuvable'}, status=404)
    reg.delete()
    return Response(status=204)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    events             = Event.objects.filter(organizer=request.user)
    total_participants = sum(e.registrations.count() for e in events)
    return Response({
        'events_count':       events.count(),
        'participants_count': total_participants,
        'revenue':            0,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_participants(request, pk):
    try:
        event = Event.objects.get(pk=pk, organizer=request.user)
    except Event.DoesNotExist:
        return Response({'detail': 'Introuvable'}, status=404)
    regs = Registration.objects.filter(event=event).select_related('user')
    return Response(RegistrationSerializer(regs, many=True).data)