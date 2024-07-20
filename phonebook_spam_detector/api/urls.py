from django.urls import path
from .views import UserCreate, LoginView, ContactListCreateView, ContactDetailView, SpamReportView, ContactSearchView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('contacts/', ContactListCreateView.as_view(), name='contacts-list-create'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('report-spam/', SpamReportView.as_view(), name='report-spam'),
    path('contacts/search/', ContactSearchView.as_view(), name='contact-search'),

]
