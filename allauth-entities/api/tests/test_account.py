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

    def test_create_account(self):
        """
        Happy Path: Create an acccount.
        Return Status: 201
        """
        url = '/accounts/'
        data = {
            "name": "New Account",
            "domain": "newexample.com",
            "subdomain": "newtest"
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201) # Verify the response status is success. this is a happy path test.
        self.assertEqual(Account.objects.count(), 2)  # Verify the practice count has the expected number in the db
       
    def test_get_account(self):
        """
        Happy Path: Get an account.
        Return Status: 200
        """
        url = f'/accounts/{self.account.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # Verify the response status is success. this is a happy path test.
        self.assertEqual(response.data['name'], self.account.name)  # Verify the retrieved account data

    def test_update_account(self):
        """
        Happy Path: Update an account.
        Return Status: 200
        """
        url = f'/accounts/{self.account.id}/'
        data = {
            "name": "Updated Account",
            "domain": "updatedexample.com",
            "subdomain": "updatedtest"
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200) # Verify the response status is success. this is a happy path test.
        self.assertEqual(response.data['name'], data['name'])  # Verify the updated account data

    def test_delete_account(self):
        """
        Happy Path: Delete an account.
        Return Status: 204
        """
        url = f'/accounts/{self.account.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204) # Verify the response status is success. this is a happy path test.
        self.assertEqual(Account.objects.count(), 0)  # Verify the account is deleted

