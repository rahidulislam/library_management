from rest_framework import serializers
from account.models import MemberApplication

class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'nid', 'birth_registration', 'image', 'is_approved', )