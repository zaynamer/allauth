from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from api.account.models import Account
from api.practice.models import Practice

class PracticeAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        test_username='user1'
        test_password='testpassword'
        self.account1 = Account.objects.create(name='Test Account 1', domain='example.com', subdomain='test')
        self.user1 = get_user_model().objects.create(username=test_username, password=test_password)
        self.account1.users.add(self.user1)
        self.client.force_login(self.user1)
        self.practice = Practice.objects.create(
            name='Test Practice', 
            type='SomePracticeType', 
            email='practice@example.com', 
            account_id=self.account1.id) # When creating an entity in code, you must include the tenant foreign key, account_id.
                                        # Within this test is the only time a Entity should be created by code. 
                                        # All other calls must go through the API endpoint

    def tearDown(self):
        if self.practice:
            self.practice.delete()
        if self.account1:
            self.account1.delete()
        if self.user1:
            self.user1.delete()
        self.client.logout()

    def test_create_practice(self):
        """
        Happy Path: Create a practice.
        Return Status: 201
        """
        url = '/practices/'
        new_practice_name = "New Practice"
        new_practice_type = "AnotherPracticeType"
        new_practice_email = "practiceemail@example.com"
        data = {
            "name": new_practice_name,
            "type": new_practice_type,
            "email": new_practice_email
        }
        response = self.client.post(url, data, content_type='application/json') # When creating an entity via API, 
                            #the account_id will be retrieved from their user info.
        self.assertEqual(response.status_code, 201) # Verify the response status is success. this is a happy path test.
        self.assertEqual(response.data["name"], new_practice_name) # Verify the created practice name
        self.assertEqual(Practice.objects.count(), 2)  # Verify the practice count has the expected number in the db

    def test_get_practice(self):
        """
        Happy Path: Get a practice.
        Return Status: 200
        """
        url = f'/practices/{self.practice.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # Verify the response status is success. This is a happy path test.
        self.assertEqual(self.account1.id, response.data['account_id'])  # Verify tenancy by checking the retrieved account id 
        self.assertEqual(response.data['name'], self.practice.name)  # Verify the retrieved practice name

    def test_update_practice(self):
        """
        Happy Path: Update a practice.
        Return Status: 200
        """
        url = f'/practices/{self.practice.id}/'
        data = {
            "name": "Updated Practice",
            "type": "YetAnotherPracticeType",
            "email": "newpracticeemail@example.com"
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200) # Verify the response status is success. This is a happy path test.
        self.assertEqual(response.data['name'], data['name'])  # Verify the updated practice name

    def test_delete_practice(self):
        """
        Happy Path: Delete a practice.
        Return Status: 204
        """
        url = f'/practices/{self.practice.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204) # Verify the response status is success. This is a happy path test.
        self.assertEqual(Practice.objects.count(), 0)  # Verify the practice is deleted

    def test_create_practice_rejected_missing_fields(self):
        """
        Unhappy Path: Create a practice.
        Return Status: 400 Bad Request
        Reason: Missing Fields
        """
        url = '/practices/'
        new_practice_email = "practiceemail@example.com"
        data = {
            "email": new_practice_email
        }
        response = self.client.post(url, data, content_type='application/json') 
        self.assertEqual(response.status_code, 400) # Verify the response status is as expected. This is an unhappy path test.
        self.assertEqual(Practice.objects.count(), 1)  # Verify the practice count has the expected number in the db
    
    def test_create_practice_rejected_user_tenancy(self):
        """
        Unhappy Path: Create a practice.
        Return Status: 403 AuthorizationException
        Reason: Tenancy is invalid. User has no account
        """
        test_username='user_no_account'
        test_password='testpassword'
        user_no_account = get_user_model().objects.create(username=test_username, password=test_password)
        self.client.force_login(user_no_account)
        url = '/practices/'
        new_practice_name = "New Practice"
        new_practice_type = "AnotherPracticeType"
        new_practice_email = "practiceemail@example.com"
        data = {
            "name": new_practice_name,
            "type": new_practice_type,
            "email": new_practice_email
        }
        response = self.client.post(url, data, content_type='application/json') 
        self.assertEqual(response.status_code, 403) # Verify the response status is as expected. This is an unhappy path test.
        self.assertEqual(Practice.objects.count(), 1)  # Verify the practice count has the expected number in the db

