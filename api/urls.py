from django.urls import path

from . import views

urlpatterns = [
    # Authentification
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.me, name='me'),

    # Événements
    path('events/', views.EventListCreateView.as_view(), name='events'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),

    # Inscriptions
    path('events/<int:event_id>/register/', views.register_to_event, name='register-to-event'),
    path('events/<int:event_id>/participants/', views.event_participants, name='event-participants'),

    # Participant
    path('my-registrations/', views.my_registrations, name='my-registrations'),

    # Organisateur
    path('dashboard/', views.dashboard, name='dashboard'),
]
