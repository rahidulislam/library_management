from django.db import models
from django.utils import timezone
from datetime import timedelta
from backend.base import TimeStamp
from account.models import User
from library.models import LibraryBranch
# Create your models here.


class SubscriptionPlan(models.Model):
    class SubscriptionType(models.TextChoices):
        MONTHLY = "MONTHLY", "Monthly"
        YEARLY = "YEARLY", "Yearly"
        LIFETIME = "LIFETIME", "Lifetime"

    library_branch = models.ForeignKey(
        "library.LibraryBranch", on_delete=models.CASCADE, related_name="subscription_plans"
    )
    name = models.CharField(max_length=100)
    subscription_type = models.CharField(
        max_length=20, choices=SubscriptionType.choices
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField(
        help_text="Duration of the plan in months. For lifetime, set it to a high number like 999."
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Member(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    # library_branch = models.ForeignKey(
    #     LibraryBranch, on_delete=models.CASCADE, related_name="members"
    # )
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    def get_subscription_plan(self):
        return MemberSubscription.objects.get(member=self)


class MemberSubscription(models.Model):
    member = models.OneToOneField(
        "Member", on_delete=models.CASCADE, related_name="subscription"
    )
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(
                days=30 * self.subscription_plan.duration_months
            )
        super().save(*args, **kwargs)

    def is_active(self):
        return self.end_date >= timezone.now().date()

    def __str__(self):
        return f"{self.member.user.email} - {self.subscription_plan.name}"


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
    # library_branch = models.ForeignKey(
    #     LibraryBranch, on_delete=models.CASCADE, related_name="member_applications"
    # )
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="member_applications")
    reject_feedback = models.TextField(blank=True)

    class Meta:
        verbose_name = "Member Application"
        verbose_name_plural = "Member Applications"

    def __str__(self):
        return self.user.email
