from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer, SignupSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from .permissions import IsOrganizerOrAdmin,IsAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CurrentUserSerializer

# Signup
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response




# List all Events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Event Detail (single event by ID)
class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer





# Register for an Event
class RegistrationCreateView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

# List all my Registrations
class RegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(student=self.request.user)

# Cancel a Registration
class RegistrationDeleteView(generics.DestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrAdmin]


class CurrentUserView(APIView):
    """
    GET /api/users/me/  -> returns current user info including role
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # If userprofile is missing for some reason, try creating default (optional)
        try:
            _ = user.userprofile
        except Exception:
            # optional: lazy-create a userprofile if you have that model
            from .models import UserProfile
            UserProfile.objects.get_or_create(user=user)
        serializer = CurrentUserSerializer(user, context={'request': request})
        return Response(serializer.data)

# Update an Event (organizer/admin only)
class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrAdmin]


# Delete an Event (organizer/admin only)
class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrAdmin]


class AdminOnlyView(APIView):
    """
    Example endpoint only accessible by admins
    """
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all().values("id", "username", "email")
        return Response({"message": "Hello Admin!", "users": list(users)})