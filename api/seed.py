import os, sys, django
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User, Event

print("🌱 Création des données...")

org, _ = User.objects.get_or_create(username='organisateur_main', defaults={
    'email': 'organisateur@eventify.com', 'first_name': 'Amadou',
    'last_name': 'Diallo', 'role': 'organizer',
})
org.set_password('test1234')
org.save()
print(f"✅ Organisateur créé")

part, _ = User.objects.get_or_create(username='participant_main', defaults={
    'email': 'participant@eventify.com', 'first_name': 'Fatou',
    'last_name': 'Sow', 'role': 'participant',
})
part.set_password('test1234')
part.save()
print(f"✅ Participant créé")

EVENTS = [
    { 'title': "TechTalk Dakar — L'IA en Afrique 2025",
      'description': "Conférence sur l'IA en Afrique. Keynotes, tables rondes, networking.",
      'location': 'Radisson Blu Hotel, Dakar', 'date': datetime.now() + timedelta(days=15),
      'category': 'conference', 'capacity': 300, 'price': 15000, 'is_private': False },

    { 'title': 'Concert Afrobeats Night — Dakar Live',
      'description': "La plus grande nuit afrobeats de l'année !",
      'location': 'Grand Théâtre National, Dakar', 'date': datetime.now() + timedelta(days=22),
      'category': 'concert', 'capacity': 1500, 'price': 25000, 'is_private': False },

    { 'title': 'Atelier Design Thinking & Innovation',
      'description': 'Apprenez le Design Thinking utilisé par les grandes entreprises.',
      'location': 'CTIC Dakar, Almadies', 'date': datetime.now() + timedelta(days=8),
      'category': 'atelier', 'capacity': 40, 'price': 0, 'is_private': False },

    { 'title': 'Marathon Dakar 2025 — Course Populaire',
      'description': 'Parcours 5km, 10km et 21km ouverts à tous !',
      'location': "Place de l'Indépendance, Dakar", 'date': datetime.now() + timedelta(days=30),
      'category': 'sport', 'capacity': 2000, 'price': 5000, 'is_private': False },

    { 'title': 'Networking Entrepreneurs Dakar 2025',
      'description': "Rencontrez les entrepreneurs et investisseurs de l'écosystème sénégalais.",
      'location': 'Sofitel Dakar Terrou-Bi', 'date': datetime.now() + timedelta(days=12),
      'category': 'networking', 'capacity': 150, 'price': 10000, 'is_private': False },

    { 'title': 'Masterclass Photographie Mobile 2025',
      'description': 'Transformez votre smartphone en appareil photo professionnel !',
      'location': 'Institut Français de Dakar', 'date': datetime.now() + timedelta(days=5),
      'category': 'atelier', 'capacity': 25, 'price': 0, 'is_private': False },

    { 'title': 'Forum Femmes Leaders Afrique 2025',
      'description': 'Forum dédié aux femmes leaders africaines.',
      'location': 'King Fahd Palace, Dakar', 'date': datetime.now() + timedelta(days=45),
      'category': 'conference', 'capacity': 500, 'price': 20000, 'is_private': False },

    { 'title': 'Hackathon FinTech Sénégal 2025',
      'description': '48h pour imaginer les solutions fintech de demain. Prix : 5M FCFA.',
      'location': 'Orange Digital Center, Dakar', 'date': datetime.now() + timedelta(days=18),
      'category': 'conference', 'capacity': 200, 'price': 0, 'is_private': False },
]

created = 0
for ev in EVENTS:
    if not Event.objects.filter(title=ev['title']).exists():
        Event.objects.create(organizer=org, **ev)
        print(f"  ✅ {ev['title']}")
        created += 1
    else:
        print(f"  ⏭️  Déjà existant : {ev['title']}")

print(f"\n🎉 {created} événements créés ! Total : {Event.objects.count()}")
print("🔑 organisateur@eventify.com / test1234")
print("🔑 participant@eventify.com  / test1234")