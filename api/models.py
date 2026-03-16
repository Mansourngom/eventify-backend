from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=False)
    role  = models.CharField(
        max_length=20,
        choices=[('participant','Participant'),('organizer','Organizer')],
        default='participant'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_set',
        blank=True
    )

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Registration(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event      = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.participant.username} -> {self.event.title}"
