from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.lab.models import Lab
from api.account.models import Account
from api.patient.models import Patient
from api.practice.models import Practice
from django.contrib.auth import get_user_model
from datetime import date, datetime

class LabAPITestCase(TestCase):
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

        self.lab = Lab.objects.create(
            cr = 99.0,
            burn = 99.0,
            gfr = 99.0,
            alb = 99.0,
            hb = 99.0,
            hct = 99.0,
            phos = 99.0,
            ca = 99.0,
            pth = 99.0,
            p_cr_ratio = 99.0,
            account_id=self.account.id,
            patient_id=self.patient.id
        ) 
        
    def test_list_Labs(self):
        response = self.client.get('/labs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_Labs(self):
        response = self.client.get(f'/labs/{self.lab.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lab(self):
        data ={
            "date_time": "2023-08-11T07:51:00Z",
            "cr": 123.0,
            "burn": 123.0,
            "gfr": 123.0,
            "alb": 123.0,
            "hb": 123.0,
            "hct": 123.0,
            "phos": 123.0,
            "ca": 123.0,
            "pth": 123.0,
            "p_cr_ratio": 123.0,
            "patient_id": self.patient.pk,
        }
        response = self.client.post('/labs/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lab.objects.count(), 2)

    def test_update_lab(self):
        data ={
            "date_time": "2023-08-11T07:51:00Z",
            "cr": 111.0,
            "burn": 111.0,
            "gfr": 111.0,
            "alb": 111.0,
            "hb": 111.0,
            "hct": 111.0,
            "phos": 111.0,
            "ca": 111.0,
            "pth": 111.0,
            "p_cr_ratio": 111.0,
            "patient_id": self.patient.pk,
        }
        
        response = self.client.put(f'/labs/{self.lab.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lab.refresh_from_db()
        self.assertEqual(self.lab.cr, 111.0)


    def test_delete_lab(self):
        response = self.client.delete(f'/labs/{self.lab.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lab.objects.count(), 0)

    def test_create_lab_missing_fields(self):
        data = {
            "date_time": "2023-08-11T07:51:00Z",
            "cr": 111.0,
            "burn": 111.0,
            "gfr": 111.0,
        }
        response = self.client.post('/labs/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lab.objects.count(), 1)
    
    def test_update_non_existing_lab(self):
        data ={
            "date_time": "2023-08-11T07:51:00Z",
            "cr": 111.0,
            "burn": 111.0,
            "gfr": 111.0,
            "alb": 111.0,
            "hb": 111.0,
            "hct": 111.0,
            "phos": 111.0,
            "ca": 111.0,
            "pth": 111.0,
            "p_cr_ratio": 111.0,
            "patient_id": self.patient.pk,
        }
        non_existing_lab_id = self.lab.pk + 1
        response = self.client.put(f'/labs/{non_existing_lab_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    