from datetime import date
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.practitioner.models import Practitioner
from api.practice.models import Practice
from api.account.models import Account
from django.contrib.auth import get_user_model

class PractitionerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create(name='Test Account 1', domain='example.com', subdomain='test')
        self.practice = Practice.objects.create(
            name='Test Practice', 
            type='SomePracticeType', 
            email='practice@example.com', 
            account_id=self.account.id
        )
        
        self.user = get_user_model().objects.create(username='test_username', password='test_password')
        self.account.users.add(self.user) 
        self.client.force_login(self.user)

        self.practitioner = Practitioner.objects.create(
            first_name='New',
            last_name='Practitioner',
            gender='male',
            birthdate = date.today(),
            address="123 Main St",
            city="Anytown",
            state="Idaho",
            zipcode="87654",
            contact='1234567890',
            active=True,
            qualification='Test Qualification',
            fhir_resource_id='1',
            account_id=self.account.id
        )
        # Associate the practice with the practitioner (many-to-many relationship)
        self.practitioner.practices.add(self.practice)

    def test_list_practitioners(self):
        response = self.client.get('/practitioners/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_practitioner(self):
        response = self.client.get(f'/practitioners/{self.practitioner.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_practitioner(self):

        data = {
            "first_name":'New',
            "last_name":'Practitioner2',
            "gender":'male',
            "birthdate" : date.today(),
            "address":"123 Main St",
            "city":"Anytown",
            "state":"Idaho",
            "zipcode":"87654",
            'contact': '9876543210',
            'active': True,
            'qualification': 'New Qualification',
            'fhir_resource_id': '1',
            'practices': [self.practice.pk],
        }
        response = self.client.post('/practitioners/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["account_id"], self.account.id)
        self.assertEqual(Practitioner.objects.count(), 2)

    def test_update_practitioner(self):
        data = {
            "first_name":'New',
            "last_name":'Practitioner2',
            "gender":'male',
            "birthdate" : date.today(),
            "address":"123 Main St",
            "city":"Anytown",
            "state":"Idaho",
            "zipcode":"87654",
            'contact': '9876543210',
            'active': False,
            'qualification': 'Updated Qualification',
            'fhir_resource_id': '1',       
            'practices': [self.practice.pk],  # Use the new field name 'practice' for the many-to-many relationship
        }
        response = self.client.put(f'/practitioners/{self.practitioner.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.practitioner.refresh_from_db()
        self.assertEqual(str(self.practitioner), self.practitioner.first_name + " " + self.practitioner.last_name)
        self.assertEqual(self.practitioner.qualification, 'Updated Qualification')

    def test_delete_practitioner(self):
        response = self.client.delete(f'/practitioners/{self.practitioner.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Practitioner.objects.count(), 0)

    def test_update_non_existing_practitioner(self):
        data = {
            "first_name":'New',
            "last_name":'Practitioner2',
            "gender":'male',
            "birthdate" : date.today(),
            "address":"123 Main St",
            "city":"Anytown",
            "state":"Idaho",
            "zipcode":"87654",
            'contact': '9876543210',
            'active': False,
            'qualification': 'Updated Qualification',
            'fhir_resource_id': '1',
            'practice': [self.practice.pk],  # Use the new field name 'practice' for the many-to-many relationship
        }
        non_existing_practitioner_id = self.practitioner.pk + 1
        response = self.client.put(f'/practitioners/{non_existing_practitioner_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
