from .models import User, Contact
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import generics, status, filters
from .serializers import ContactSerializer, SpamReportSerializer
from django.db import models  # Add this import


# from rest_framework.permissions import IsAuthenticated

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ContactListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class SpamReportView(generics.GenericAPIView):
    serializer_class = SpamReportSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        contact = Contact.objects.get(phone_number=phone_number)
        contact.spam_reports += 1
        if contact.spam_reports > 2:  # Example threshold for marking as spam
            contact.is_spam = True
        contact.save()
        return Response({"status": "reported"}, status=status.HTTP_200_OK)


class ContactSearchView(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contact.objects.filter(user=self.request.user)
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(phone_number__icontains=query) |
                models.Q(email__icontains=query)
            )
        return queryset