from django.db import models
from django.contrib.auth.models import AbstractUser
from backend.base import TimeStamp

# Create your models here.
class User(AbstractUser):
    ADMIN = 1
    MEMBER = 2
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)


class Profile(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    image = models.ImageField(upload_to="profile", blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username