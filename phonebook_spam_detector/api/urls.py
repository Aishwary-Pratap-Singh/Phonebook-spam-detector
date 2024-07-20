from django.urls import path
from .views import UserCreate, LoginView, ContactListCreateView, ContactDetailView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('contacts/', ContactListCreateView.as_view(), name='contacts-list-create'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),]
