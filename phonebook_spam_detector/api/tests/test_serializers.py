from django.test import TestCase
from ..models import User, Contact
from ..serializers import ContactSerializer

class ContactSerializerTests(TestCase):

    def test_serialize_contact(self):
        user = User.objects.create_user(username='testuser', password='testpassword', phone_number='1234567890', email='test@example.com')
        contact = Contact.objects.create(user=user, name='John Doe', phone_number='1234567890', email='john@example.com')
        serializer = ContactSerializer(contact)
        data = serializer.data
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['phone_number'], '1234567890')
