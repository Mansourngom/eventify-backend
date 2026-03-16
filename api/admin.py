from django.contrib import admin
<<<<<<< Updated upstream

# Register your models here.
=======
from .models import User, Event, Registration

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Registration)
>>>>>>> Stashed changes
