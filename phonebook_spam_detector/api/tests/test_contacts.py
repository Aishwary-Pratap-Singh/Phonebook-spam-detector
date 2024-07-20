from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User, Contact


class ContactTests(APITestCase):

    def setUp(self):
        # Create a user and obtain JWT token
        self.user = User.objects.create_user(username='testuser', password='testpassword', phone_number='1234567890',
                                             email='test@example.com')
        self.client.login(username='testuser', password='testpassword')

        # Add token to the client
        self.client.force_authenticate(user=self.user)

    def test_create_contact(self):
        url = reverse('contacts-list-create')
        data = {
            'name': 'John Doe',
            'phone_number': '1234567890',
            'email': 'john@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, 'John Doe')

    def test_list_contacts(self):
        Contact.objects.create(user=self.user, name='John Doe', phone_number='1234567890', email='john@example.com')
        url = reverse('contacts-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_retrieve_contact(self):
        contact = Contact.objects.create(user=self.user, name='John Doe', phone_number='1234567890',
                                         email='john@example.com')
        url = reverse('contact-detail', args=[contact.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_update_contact(self):
        contact = Contact.objects.create(user=self.user, name='John Doe', phone_number='1234567890',
                                         email='john@example.com')
        url = reverse('contact-detail', args=[contact.id])
        data = {
            'name': 'John Doe Updated',
            'phone_number': '0987654321',
            'email': 'john.updated@example.com',
            'is_spam': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'John Doe Updated')
        self.assertEqual(contact.phone_number, '0987654321')
        self.assertEqual(contact.email, 'john.updated@example.com')
        self.assertEqual(contact.is_spam, True)

    def test_delete_contact(self):
        contact = Contact.objects.create(user=self.user, name='John Doe', phone_number='1234567890',
                                         email='john@example.com')
        url = reverse('contact-detail', args=[contact.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)
