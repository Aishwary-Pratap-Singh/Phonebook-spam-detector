from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserTests(APITestCase):

    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('register')
        data = {
            'username': 'testuser',
            'phone_number': '1234567890',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().phone_number, '1234567890')
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_create_user_without_phone_number(self):
        """
        Ensure we can't create a user without a phone number.
        """
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class UserAuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', phone_number='1234567890', password='testpassword')

    def test_login_user(self):
        """
        Ensure we can log in a user with valid credentials.
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
