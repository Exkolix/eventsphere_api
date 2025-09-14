from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=50)  # e.g. technical, cultural
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# models.py
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='confirmed'
    )

    class Meta:
        unique_together = ('event', 'student')  # prevent duplicate registration

    def __str__(self):
        return f"{self.student.username} -> {self.event.title}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
