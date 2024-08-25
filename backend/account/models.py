from django.db import models
from django.contrib.auth.models import AbstractUser
from backend.base import TimeStamp


# Create your models here.
class User(AbstractUser):
    class UserRoleType(models.IntegerChoices):
        ADMIN = 1, "Admin"
        MEMBER = 2, "Member"

    username = None
    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(
        choices=UserRoleType.choices, default=UserRoleType.MEMBER
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Profile(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    nid = models.CharField(max_length=17, unique=True, blank=True)
    birth_registration = models.CharField(max_length=100, unique=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_images", blank=True)

    def __str__(self):
        return self.user.email


class MemberShip(TimeStamp):
    class MembershipType(models.TextChoices):
        REGULAR = "Regular", "Regular"
        PREMIUM = "Premium", "Premium"

    membership_type = models.CharField(
        max_length=50, choices=MembershipType.choices, default=MembershipType.REGULAR
    )
