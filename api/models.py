from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=20, default='participant')

class Event(models.Model):
    CATEGORIES = [('conference','Conférence'),('concert','Concert'),('atelier','Atelier'),
                  ('sport','Sport'),('networking','Networking'),('autre','Autre')]
    title       = models.CharField(max_length=200)
    description = models.TextField()
    location    = models.CharField(max_length=200)
    date        = models.DateTimeField()
    image       = models.ImageField(upload_to='events/', null=True, blank=True)
    category    = models.CharField(max_length=50, choices=CATEGORIES, default='conference')
    is_private  = models.BooleanField(default=False)
    capacity    = models.IntegerField(default=100)
    price       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    organizer   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    created_at  = models.DateTimeField(auto_now_add=True)

class Registration(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event      = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'event')