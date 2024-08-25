from rest_framework import serializers
from membership.models import MemberApplication, SubscriptionPlan

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"

class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = (
            "subscription_plan",
            
        )

class MemberApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = ('id', 'user', 'subscription_plan','status','reject_feedback','created_at',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.email
        data['subscription_plan'] = instance.subscription_plan.name
        return data