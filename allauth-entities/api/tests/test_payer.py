from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.practice.models import Practice
from api.account.models import Account
from api.payer.models import Payer
from django.contrib.auth import get_user_model

class PayerAPITestCase(TestCase):
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

        self.payer = Payer.objects.create(
            payer_name='Test Payer',
            active=True,
            description='Test Description',
            contact='Test Contact',
            qualification='Test Qualification',
            alias='Test Alias',
            fhir_resource_id='Test FHIR Resource ID',
            account_id=self.account.id
        )
        self.payer.practice.add(self.practice)

    def test_list_payers(self):
        response = self.client.get('/payers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_payer(self):
        response = self.client.get(f'/payers/{self.payer.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payer(self):
        data = {
            'payer_name': 'New Payer',
            'active': True,
            'description': 'New Description',
            'contact': 'New Contact',
            'qualification': 'New Qualification',
            'alias': 'New Alias',
            'fhir_resource_id': 'New FHIR Resource ID',
            'practice': [self.practice.pk]
        }
        response = self.client.post('/payers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["account_id"], self.account.id)
        self.assertEqual(Payer.objects.count(), 2)

    def test_update_payer(self):
        data = {
            'payer_name': 'Updated Payer',
            'active': False,
            'description': 'Updated Description',
            'contact': 'Updated Contact',
            'qualification': 'Updated Qualification',
            'alias': 'Updated Alias',
            'fhir_resource_id': 'Updated FHIR Resource ID',
            'practice': [self.practice.pk]
        }
        response = self.client.put(f'/payers/{self.payer.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payer.refresh_from_db()
        self.assertEqual(self.payer.payer_name, 'Updated Payer')

    def test_delete_payer(self):
        response = self.client.delete(f'/payers/{self.payer.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payer.objects.count(), 0)


    def test_create_payer_missing_fields(self):
        data = {
            # Missing required field 'payer_name'
            'active': True,
            'description': 'New Description',
            'contact': 'New Contact',
            'qualification': 'New Qualification',
            'alias': 'New Alias',
            'fhir_resource_id': 'New FHIR Resource ID',
            'practice': [self.practice.pk]
        }
        response = self.client.post('/payers/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Payer.objects.count(), 1)

    def test_update_payer_invalid_practice(self):
        data = {
            'payer_name': 'Updated Payer',
            'active': False,
            'description': 'Updated Description',
            'contact': 'Updated Contact',
            'qualification': 'Updated Qualification',
            'alias': 'Updated Alias',
            'fhir_resource_id': 'Updated FHIR Resource ID',
            # Use an invalid practice ID that does not exist
            'practice': [self.practice.pk+1]
        }
        response = self.client.put(f'/payers/{self.payer.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.payer.refresh_from_db()
        self.assertNotEqual(self.payer.payer_name, 'Updated Payer')