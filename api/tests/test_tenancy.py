from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from api.account.models import Account
from api.practice.models import Practice

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(username='superuser', password='testpassword')
        self.client.force_login(user=self.superuser)
        self.account1 = Account.objects.create(name='Account 1', domain='example1.com', subdomain='account1')
        self.account2 = Account.objects.create(name='Account 2', domain='example2.com', subdomain='account2')
        self.user1 = get_user_model().objects.create(username='user1', password='testpassword')
        self.user2 = get_user_model().objects.create(username='user2', password='testpassword')
        self.account1.users.add(self.user1)
        self.account2.users.add(self.user2)
        self.practice1 = Practice.objects.create(
            name='Test Practice 1', 
            type='SomePractice1Type', 
            email='practice1@example.com',
            account_id=self.account1.id
        )
        self.practice2 = Practice.objects.create(
            name='Test Practice 2', 
            type='SomePractice2Type', 
            email='practice2@example.com',
            account_id=self.account2.id
        )

    def tearDown(self):
        self.client.logout()

    def test_superuser_can_see_all_practices(self):
        """
        Happy Path: View all entities because superuser.
        Return Status: 200
        """
        self.client.force_login(user=self.superuser)
        url = '/practices/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Verify the response status is success. 
        self.assertEqual(response.data["count"], 2)  # Verify that all practices are returned

    def test_user_can_only_see_own_practice(self):
        """
        Happy Path: View single user entities because tenancy is applied.
        Return Status: 200
        """
        self.client.force_login(user=self.user1)
        url = '/practices/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Verify the response status is success. 
        self.assertEqual(response.data["count"], 1)  # Verify that only the expected number of practices are returned
        self.assertEqual(response.data["results"][0]['name'], self.practice1.name)  # Verify the practice name

    def test_user_cannot_see_practices_not_assigned_to_them(self):
        """
        Happy Path: View single user entities because tenancy is applied.
        Return Status: 404
        """
        self.client.force_login(user=self.user2)
        url = f'/practices/{self.practice1.id}'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404) # Verify the response status is unauthorized. 


    def test_user_in_multiple_accounts_has_first_active_account_working(self):
        """
        Happy Path: Set user's active_account_id and get valid entity
        Return Status: 200
        """
        self.account1.users.add(self.user2)
        self.account1.save()
        self.user2.active_account_id = self.account1.id # Practice1 should now be available to user2
        self.user2.save()
        self.client.force_login(user=self.user2)
        url = f'/practices/{self.practice1.id}' 
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200) # Verify the response status is successful. 
        self.assertFalse(isinstance(response.data,  list))  # Verify only one practice is returned

    def test_user_in_multiple_accounts_has_second_active_account_working(self):
        """
        Happy Path: Set user's active_account_id and get invalid then valid entity
        Return Status: 404, 200
        """
        self.account1.users.add(self.user2)
        self.account1.save()
        self.user2.active_account_id = self.account2.id # Practice2 should now be available to user2
        self.user2.save()
        self.client.force_login(user=self.user2)
        url = f'/practices/{self.practice1.id}'      # Try to get practice1
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)  # Verify the response status is unsuccessful. 
        url = f'/practices/{self.practice2.id}'      # Try to get practice2
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)  # Verify the response status is successful. 
        self.assertFalse(isinstance(response.data,  list))  # Verify only one practice is returned
        
