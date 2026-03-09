from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Event, Profile


class EventVisibilityTests(APITestCase):
    def setUp(self):
        self.organizer_1 = User.objects.create_user(username='org1', password='pass1234')
        self.organizer_2 = User.objects.create_user(username='org2', password='pass1234')
        Profile.objects.create(user=self.organizer_1, role='organizer')
        Profile.objects.create(user=self.organizer_2, role='organizer')

        self.public_event = Event.objects.create(
            title='Public Event',
            description='Visible to everyone',
            location='Paris',
            date=timezone.now(),
            is_public=True,
            organizer=self.organizer_1,
        )
        self.private_event_org1 = Event.objects.create(
            title='Private Org1',
            description='Private 1',
            location='Lyon',
            date=timezone.now(),
            is_public=False,
            organizer=self.organizer_1,
        )
        self.private_event_org2 = Event.objects.create(
            title='Private Org2',
            description='Private 2',
            location='Marseille',
            date=timezone.now(),
            is_public=False,
            organizer=self.organizer_2,
        )

    def test_anonymous_user_only_sees_public_events(self):
        response = self.client.get('/api/events/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item['id'] for item in response.data}
        self.assertIn(self.public_event.id, returned_ids)
        self.assertNotIn(self.private_event_org1.id, returned_ids)
        self.assertNotIn(self.private_event_org2.id, returned_ids)

    def test_authenticated_user_sees_public_and_own_private_events(self):
        self.client.force_authenticate(user=self.organizer_1)
        response = self.client.get('/api/events/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item['id'] for item in response.data}
        self.assertIn(self.public_event.id, returned_ids)
        self.assertIn(self.private_event_org1.id, returned_ids)
        self.assertNotIn(self.private_event_org2.id, returned_ids)


class EventPermissionsTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass1234')
        self.other_user = User.objects.create_user(username='other', password='pass1234')
        Profile.objects.create(user=self.owner, role='organizer')
        Profile.objects.create(user=self.other_user, role='participant')

        self.public_event = Event.objects.create(
            title='Owner Public Event',
            description='Public',
            location='Paris',
            date=timezone.now(),
            is_public=True,
            organizer=self.owner,
        )
        self.private_event = Event.objects.create(
            title='Owner Private Event',
            description='Private',
            location='Lille',
            date=timezone.now(),
            is_public=False,
            organizer=self.owner,
        )

    def test_non_owner_cannot_update_event(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(
            f'/api/events/{self.public_event.id}/',
            {'title': 'Hacked title'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_owner_cannot_register_to_private_event(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(f'/api/events/{self.private_event.id}/register/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
