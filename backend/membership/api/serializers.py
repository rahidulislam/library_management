from rest_framework import serializers
from membership.models import MemberApplication, SubscriptionPlan,Member,MemberSubscription

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

class MemberSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberSubscription
        fields = ('id', 'subscription_plan', 'start_date', 'end_date')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['subscription_plan'] = instance.subscription_plan.name
        data['subscription_type'] = instance.subscription_plan.subscription_type
        data['subscription_pice'] = instance.subscription_plan.price
        data['library'] = instance.subscription_plan.library_branch.library.name
        data['library_branch'] = instance.subscription_plan.library_branch.name
        return data


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'user', 'membership_date',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.email
        data['subscription_plan'] = MemberSubscriptionSerializer(instance.get_subscription_plan()).data
        return data