# api/management/commands/create_dummy_data.py

from django.core.management.base import BaseCommand
from api.models import User, Contact

class Command(BaseCommand):
    help = 'Create dummy data for testing APIs'

    def handle(self, *args, **kwargs):
        # Delete existing data
        User.objects.all().delete()
        Contact.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all existing users and contacts'))

        # Create dummy users
        users = [
            {'username': 'user1', 'phone_number': '1234567891', 'email': 'user1@example.com', 'password': 'password1'},
            {'username': 'user2', 'phone_number': '1234567892', 'email': 'user2@example.com', 'password': 'password2'},
            {'username': 'user3', 'phone_number': '1234567893', 'email': 'user3@example.com', 'password': 'password3'},
        ]

        for user_data in users:
            user = User.objects.create_user(
                username=user_data['username'],
                phone_number=user_data['phone_number'],
                email=user_data['email'],
                password=user_data['password']
            )
            self.stdout.write(self.style.SUCCESS(f'Created user {user.username}'))

        # Create dummy contacts
        contacts = [
            {'user': User.objects.get(username='user1'), 'name': 'Contact1', 'phone_number': '2234567891', 'email': 'contact1@example.com', 'is_spam': False},
            {'user': User.objects.get(username='user2'), 'name': 'Contact2', 'phone_number': '2234567892', 'email': 'contact2@example.com', 'is_spam': False},
            {'user': User.objects.get(username='user3'), 'name': 'Contact3', 'phone_number': '2234567893', 'email': 'contact3@example.com', 'is_spam': False},
        ]

        for contact_data in contacts:
            contact = Contact.objects.create(
                user=contact_data['user'],
                name=contact_data['name'],
                phone_number=contact_data['phone_number'],
                email=contact_data['email'],
                is_spam=contact_data['is_spam']
            )
            self.stdout.write(self.style.SUCCESS(f'Created contact {contact.name} for user {contact.user.username}'))

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
