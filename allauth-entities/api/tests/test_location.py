from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.location.models import Location
from api.account.models import Account
from api.practice.models import Practice
from django.contrib.auth import get_user_model


class LocationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create(name='Test Account 1', domain='example.com', subdomain='test')
        self.practice = Practice.objects.create(
            name='Test Practice', 
            type='SomePracticeType', 
            email='practice@example.com', 
            account_id=self.account.id)
        
        self.user = get_user_model().objects.create(username='test_username', password='test_password')
        self.account.users.add(self.user) 
        self.client.force_login(self.user)
        self.location = Location.objects.create(
            location_name='Test Location',
            phone='1234567890',
            description='Test Description',
            address='Test Address',
            hours_of_operation='Test Hours',
            fhir_resource_id='test_resource',
            status=Location.StatusOptions.ACTIVE,
            practice_id=self.practice.id,
            account_id=self.account.id
        )

    def test_list_locations(self):
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_location(self):
        response = self.client.get(f'/locations/{self.location.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_location(self):
        data = {
            'location_name': 'New Location',
            'phone': '9876543210',
            'description': 'New Description',
            'address': 'New Address',
            'hours_of_operation': 'New Hours',
            'fhir_resource_id': 'new_resource',
            'status': Location.StatusOptions.ACTIVE,
            'practice_id': self.practice.pk,
        }
        response = self.client.post('/locations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

    def test_update_location(self):
        data = {
            'location_name': 'Updated Location',
            'phone': '9876543210',
            'description': 'Updated Description',
            'address': 'Updated Address',
            'hours_of_operation': 'Updated Hours',
            'fhir_resource_id': 'updated_resource',
            'status': Location.StatusOptions.INACTIVE,
            'practice_id': self.practice.pk,
        }
        response = self.client.put(f'/locations/{self.location.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.location.refresh_from_db()
        self.assertEqual(self.location.location_name, 'Updated Location')

    def test_delete_location(self):
        response = self.client.delete(f'/locations/{self.location.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 0)

    def test_create_location_missing_fields(self):
        data = {
        'location_name': 'New Location',
        'phone': '9876543210',
        'description': 'New Description',
        'hours_of_operation': 'New Hours',
        'status': Location.StatusOptions.ACTIVE,
    }
        response = self.client.post('/locations/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 1)
        
        
    def test_update_non_existing_location(self):
        data = {
        'location_name': 'Updated Location',
        'phone': '9876543210',
        'description': 'Updated Description',
        'address': 'Updated Address',
        'hours_of_operation': 'Updated Hours',
        'fhir_resource_id': 'updated_resource',
        'status': Location.StatusOptions.INACTIVE,
        'practice_id': self.practice.pk,
    }
        non_existing_location_id = self.location.pk + 1
        response = self.client.put(f'/locations/{non_existing_location_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    