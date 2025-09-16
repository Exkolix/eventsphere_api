from django.urls import path
from .views import (
    SignupView,
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,   
    EventDeleteView,   
    RegistrationCreateView,
    RegistrationListView,
    RegistrationDeleteView,
    CurrentUserView,
    AdminOnlyView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Auth
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('admin/users/', AdminOnlyView.as_view(), name='admin-users'),

    # Events
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),

    # Registrations
    path('events/register/', RegistrationCreateView.as_view(), name='register-event'),
    path('registrations/', RegistrationListView.as_view(), name='registration-list'),
    path('registrations/<int:pk>/cancel/', RegistrationDeleteView.as_view(), name='registration-cancel'),
]

