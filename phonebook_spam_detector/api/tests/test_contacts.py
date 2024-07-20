from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User, Contact


class ContactTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', phone_number='1234567890',
                                             email='test@example.com')
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.contact = Contact.objects.create(user=self.user, name='John Doe', phone_number='1234567890',
                                              email='john@example.com')

    def test_create_contact(self):
        url = reverse('contacts-list-create')
        data = {
            'name': 'Jane Doe',
            'phone_number': '0987654321',
            'email': 'jane@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.get(pk=2).name, 'Jane Doe')

    def test_list_contacts(self):
        url = reverse('contacts-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_retrieve_contact(self):
        url = reverse('contact-detail', args=[self.contact.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_update_contact(self):
        url = reverse('contact-detail', args=[self.contact.id])
        data = {
            'name': 'John Doe Updated',
            'phone_number': '0987654321',
            'email': 'john.updated@example.com',
            'is_spam': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'John Doe Updated')
        self.assertEqual(self.contact.phone_number, '0987654321')
        self.assertEqual(self.contact.email, 'john.updated@example.com')
        self.assertEqual(self.contact.is_spam, True)

    def test_delete_contact(self):
        url = reverse('contact-detail', args=[self.contact.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)

    def test_report_spam(self):
        url = reverse('report-spam')
        data = {
            'phone_number': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.spam_reports, 1)
        self.assertFalse(self.contact.is_spam)

        # Report spam again to exceed threshold
        self.client.post(url, data, format='json')
        self.client.post(url, data, format='json')
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.spam_reports, 3)
        self.assertTrue(self.contact.is_spam)


class ContactSearchTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', phone_number='1234567890', email='test@example.com')
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.contact1 = Contact.objects.create(user=self.user, name='John Doe', phone_number='1234567890', email='john@example.com')
        self.contact2 = Contact.objects.create(user=self.user, name='Jane Smith', phone_number='0987654321', email='jane@example.com')

    def test_search_contacts_by_name(self):
        url = reverse('contact-search')
        response = self.client.get(url, {'q': 'John'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_search_contacts_by_phone_number(self):
        url = reverse('contact-search')
        response = self.client.get(url, {'q': '0987654321'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['phone_number'], '0987654321')

    def test_search_contacts_by_email(self):
        url = reverse('contact-search')
        response = self.client.get(url, {'q': 'jane@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'jane@example.com')

    def test_search_contacts_no_results(self):
        url = reverse('contact-search')
        response = self.client.get(url, {'q': 'Nonexistent'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)