from django.db import models
from django.contrib.auth.models import AbstractUser
from backend.base import TimeStamp
from library.models import LibraryBranch


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


class Member(TimeStamp):
    class MembershipType(models.TextChoices):
        REGULAR = "Regular", "Regular"
        PREMIUM = "Premium", "Premium"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    library_branch = models.ForeignKey(
        LibraryBranch, on_delete=models.CASCADE, related_name="members"
    )
    membership_date = models.DateField(auto_now_add=True)
    membership_type = models.CharField(
        max_length=50, choices=MembershipType.choices, default=MembershipType.REGULAR
    )

    def __str__(self):
        return self.user.username


class MemberApplication(TimeStamp):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="member_application",
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    reject_feedback = models.TextField(blank=True)

    class Meta:
        verbose_name = "Member Application"
        verbose_name_plural = "Member Applications"

    def __str__(self):
        return self.first_name + " " + self.last_name
