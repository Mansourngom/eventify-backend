from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/',  views.register, name='register'),
    path('auth/login/',     views.login,    name='login'),
    path('auth/me/',        views.me,       name='me'),

    path('events/',                          views.event_list,        name='event-list'),
    path('events/create/',                   views.event_create,      name='event-create'),
    path('events/<int:pk>/',                 views.event_detail,      name='event-detail'),
    path('events/<int:pk>/update/',          views.event_update,      name='event-update'),
    path('events/<int:pk>/delete/',          views.event_delete,      name='event-delete'),
    path('events/<int:pk>/register/',        views.event_register,    name='event-register'),
    path('events/<int:pk>/participants/',    views.event_participants, name='event-participants'),

    path('registrations/',                   views.my_registrations,    name='my-registrations'),
    path('registrations/<int:pk>/cancel/',   views.cancel_registration, name='cancel-registration'),

<<<<<<< Updated upstream
    # Participant
    path('my-registrations/', views.my_registrations, name='my-registrations'),

    # Organisateur
    path('dashboard/', views.dashboard, name='dashboard'),
=======
    path('dashboard/stats/',                 views.dashboard_stats,   name='dashboard-stats'),
>>>>>>> Stashed changes
]