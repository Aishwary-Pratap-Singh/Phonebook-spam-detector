from django.test import TestCase
from .models import User, Contact

class UserModelTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword', phone_number='1234567890', email='test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))

class ContactModelTests(TestCase):

    def test_create_contact(self):
        user = User.objects.create_user(username='testuser', password='testpassword', phone_number='1234567890', email='test@example.com')
        contact = Contact.objects.create(user=user, name='John Doe', phone_number='1234567890', email='john@example.com')
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.phone_number, '1234567890')
