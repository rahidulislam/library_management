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
    nid= models.CharField(max_length=17, blank=True)
    birth_registration = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username
    
class MemberApplication(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='member_application')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    nid= models.CharField(max_length=17, blank=True)
    birth_registration = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to="member_application", blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name