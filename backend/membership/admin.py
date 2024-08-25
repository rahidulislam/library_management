from django.contrib import admin
from .models import Member, MemberSubscription, MemberApplication, SubscriptionPlan
# Register your models here.

admin.site.register(Member)
admin.site.register(MemberSubscription)
admin.site.register(MemberApplication)

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'duration_months', 'price', 'library_branch')