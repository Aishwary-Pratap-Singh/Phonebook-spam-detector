from rest_framework import serializers
from .models import User, Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'user', 'name', 'phone_number', 'email', 'is_spam')
        read_only_fields = ('user',)


class SpamReportSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not Contact.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Contact with this phone number does not exist.")
        return value