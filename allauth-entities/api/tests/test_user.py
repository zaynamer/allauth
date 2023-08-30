from django.test import TestCase
from django.test import Client
from api.account.models import Account
from django.contrib.auth import get_user_model

class AccountAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(username='superuser', password='testpassword')
        self.client.force_login(user=self.user)
        self.account = Account.objects.create(name='Test Account', domain='example.com', subdomain='test')

    def tearDown(self):
        if self.user:
            self.user.delete()
        if self.account:
            self.account.delete()

    def test_create_user(self):
        """
        Happy Path: Create a user.
        Return Status: 201
        """
        url = '/users/'
        data = {
            "username": "user1",
            "password": "user_password",
            "accounts": [self.account.id]
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201) # Verify the response status is success. this is a happy path test.
        self.assertEqual(get_user_model().objects.count(), 2)  # Verify the user count has the expected number in the db
        
    def test_add_user_to_user(self):
        """
        Happy Path: Update a practice with an account.
        Return Status: 200
        """
        url = f'/users/{self.user.id}/'
        data = {
            "username": "superuser",
            "password": "testpassword",
            "accounts": [self.account.id]
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200) # Verify the response status is success. this is a happy path test.
        self.assertEqual(response.data['accounts'][0], data['accounts'][0])  # Verify the user added the account

    def test_get_user(self):
        """
        Happy Path: Get a user.
        Return Status: 200
        """
        url = f'/users/{self.user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # Verify the response status is success. this is a happy path test.
        self.assertEqual(response.data['username'], self.user.username)  # Verify the retrieved account data

    def test_update_user(self):
        """
        Happy Path: Update a user.
        Return Status: 200
        """
        url = f'/users/{self.user.id}/'
        data = {
            "username": "new_username",
            "accounts": [self.account.id]
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200) # Verify the response status is success. this is a happy path test.
        self.assertEqual(response.data['username'], data['username'])  # Verify the updated account data

    def test_delete_user(self):
        """
        Happy Path: Delete a user.
        Return Status: 204
        """
        url = f'/users/{self.user.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204) # Verify the response status is success. this is a happy path test.
        self.assertEqual(get_user_model().objects.count(), 0)  # Verify the account is deleted

