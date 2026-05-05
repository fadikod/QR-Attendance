import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Session(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    external_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.pk and not self.valid_until:
            self.valid_until = timezone.now() + timedelta(hours=2)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() <= self.valid_until

    def __str__(self):
        return f"Session {self.date}"


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session')

    def __str__(self):
        return f"{self.user.username} — {self.session.date}"
