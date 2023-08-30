from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.vital.models import Vital
from api.account.models import Account
from api.patient.models import Patient
from api.practice.models import Practice
from django.contrib.auth import get_user_model
from datetime import date, datetime
 
class VitalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create(name='Test Account 1', domain='example.com', subdomain='test')
        
        self.practice = Practice.objects.create(
            name='Test Practice', 
            type='SomePracticeType', 
            email='practice@example.com', 
            account_id=self.account.id
        )

        self.patient = Patient.objects.create(
            first_name='New',
            last_name='Practitioner',
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

        self.user = get_user_model().objects.create(username='test_username', password='test_password')
        self.account.users.add(self.user) 
        self.client.force_login(self.user)

        self.vital = Vital.objects.create(
            height=23, 
            weight=34, 
            bmi=4.3,
            date_time = datetime.now(),
            systolic = 70,
            diastolic = 120,
            pulse = 65,
            spo2 = 45,
            temperature = 103,
            respiration_rate = 45,
            account_id=self.account.id,
            patient_id=self.patient.id
        ) 
        
    def test_list_vitals(self):
        response = self.client.get('/vitals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vitals(self):
        response = self.client.get(f'/vitals/{self.patient.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vitals(self):
        data ={
            "date_time": "2023-09-01T08:57:00Z",
            "height": 99999.0,
            "weight": 234.0,
            "systolic": 234.0,
            "diastolic": 234.0,
            "bmi": 234.0,
            "temperature": 234.0,
            "pulse": 234,
            "respiration_rate": 234,
            "spo2": 234.0,
            "patient_id": self.patient.pk,
        }
        response = self.client.post('/vitals/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vital.objects.count(), 2)

    def test_update_vital(self):
        data ={
            "date_time": "2023-09-01T08:57:00Z",
            "height": 777.0,
            "weight": 234.0,
            "systolic": 234.0,
            "diastolic": 234.0,
            "bmi": 234.0,
            "temperature": 234.0,
            "pulse": 234,
            "respiration_rate": 234,
            "spo2": 234.0,
            "patient_id": self.patient.pk,
        }
        
        response = self.client.put(f'/vitals/{self.patient.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vital.refresh_from_db()
        self.assertEqual(self.vital.height, 777.0)


    def test_delete_vitals(self):
        response = self.client.delete(f'/vitals/{self.vital.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vital.objects.count(), 0)

    def test_create_vital_missing_fields(self):
        data = {
            "date_time": "2023-09-01T08:57:00Z",
            "height": 777.0,
            "weight": 234.0,
            "systolic": 234.0, 
        }
        response = self.client.post('/vitals/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Patient.objects.count(), 1)
    
    def test_update_non_existing_patient(self):
        data ={
            "date_time": "2023-09-01T08:57:00Z",
            "height": 888.0,
            "weight": 234.0,
            "systolic": 234.0,
            "diastolic": 234.0,
            "bmi": 234.0,
            "temperature": 234.0,
            "pulse": 234,
            "respiration_rate": 234,
            "spo2": 234.0,
            "patient_id": self.patient.pk,
        }
        non_existing_patient_id = self.patient.pk + 1
        response = self.client.put(f'/patients/{non_existing_patient_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    