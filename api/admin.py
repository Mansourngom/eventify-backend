from django.contrib import admin
from .models import Event, Profile, Registration

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Registration)
