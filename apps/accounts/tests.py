from django.test import TestCase
from accounts.models import Account


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create(username='test username', password='1234EErr')
        self.superuser = Account.objects.create_superuser(username='test superuser', password='1234EErr')
    
    def test_user_token_created(self):
        '''Make sure that token is created for user'''
        self.assertNotEqual(self.user.token, None)

    def test_normal_user_role(self):
        '''By default user role is normal'''
        self.assertFalse(self.user.is_superuser)

    def test_superuser_user_role(self):
        '''Check superuser role'''
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)

    def test_user_unique_token(self):
        self.assertNotEqual(self.user.token, self.superuser.token)

    def test_user_username_is_lower(self):
        self.assertEqual(self.user.username, self.user.username.lower())