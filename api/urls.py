from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/',                views.register),
    path('auth/login/',                   views.login),
    path('auth/me/',                      views.me),
    path('events/',                       views.event_list),
    path('events/create/',                views.event_create),
    path('events/<int:pk>/',              views.event_detail),
    path('events/<int:pk>/update/',       views.event_update),
    path('events/<int:pk>/delete/',       views.event_delete),
    path('events/<int:pk>/register/',     views.event_register),
    path('events/<int:pk>/participants/', views.event_participants),
    path('registrations/',                views.my_registrations),
    path('registrations/<int:pk>/cancel/', views.cancel_registration),
    path('dashboard/stats/',              views.dashboard_stats),
]