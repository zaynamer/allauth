from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.patient.models import Patient
from api.account.models import Account
from api.practice.models import Practice
from django.contrib.auth import get_user_model
from datetime import date, datetime

class PatientAPITestCase(TestCase):
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
    
        self.patient = Patient.objects.create(
            first_name='Test',
            last_name='Patient',
            gender='male',
            birthdate = date.today(),
            address="123 Main St",
            city="Anytown",
            state="Idaho",
            zipcode="87654",
            patient_status = 0,
            pr_no = 324,
            primary_insurance = 23432,
            last_appointment = datetime.now(),
            next_appointment = datetime.now(),
            patient_balance = 2134,
            terminated = 234,
            fhir_resource_id = "fdsf",
            account_id=self.account.id
        )

        # Associate the practice with the patient (many-to-many relationship)
        self.patient.practices.add(self.practice)


    def test_list_patients(self):
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_patients(self):
        response = self.client.get(f'/patients/{self.patient.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_patient(self):

        data = {
            "first_name":'Test',
            "last_name":'Patient2',
            "gender":'male',
            "birthdate" : date.today(),
            "address":"123 Main St",
            "city":"Anytown",
            "state":"Idaho",
            "zipcode":"87654",
            "patient_status": 90,
            "pr_no": 90,
            "primary_insurance": "423erfwe",
            "last_appointment": "2023-08-27",
            "next_appointment": "2023-09-09",
            "patient_balance": 90.0,
            "terminated": 90,
            "fhir_resource_id": "23432",
            "practices": [self.practice.pk]
        }
        response = self.client.post('/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)

    def test_update_patient(self):
        data = {
            "first_name":'Test',
            "last_name":'Patient2',
            "gender":'male',
            "birthdate" : date.today(),
            "address":"123 Main St",
            "city":"Anytown",
            "state":"Idaho",
            "zipcode":"87654",
            "patient_status": 80,
            "pr_no": 80,
            "primary_insurance": "423erfwe",
            "last_appointment": "2023-08-27",
            "next_appointment": "2023-09-09",
            "patient_balance": 80.0,
            "terminated": 80,
            "fhir_resource_id": "23432",
            "practices": [self.practice.pk]
        }
        response = self.client.put(f'/patients/{self.patient.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.pr_no, 80)

    def test_delete_patient(self):
        response = self.client.delete(f'/patients/{self.patient.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)

    def test_create_patient_missing_fields(self):
        data = {
            "patient_status": 80,
            "pr_no": 80, 
        }
        response = self.client.post('/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Patient.objects.count(), 1)
        
        
    def test_update_non_existing_patient(self):
        data = {
            "first_name":'Test',
            "last_name":'Patient2',
            "gender":'male',
            "birthdate" : date.today(),
            "address":"123 Main St",
            "city":"Anytown",
            "state":"Idaho",
            "zipcode":"87654",
            "patient_status": 80,
            "pr_no": 80,
            "primary_insurance": "423erfwe",
            "last_appointment": "2023-08-27",
            "next_appointment": "2023-09-09",
            "patient_balance": 80.0,
            "terminated": 80,
            "fhir_resource_id": "23432",
            "practices": [self.practice.pk]
        }
        non_existing_patient_id = self.patient.pk + 1
        response = self.client.put(f'/patients/{non_existing_patient_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    