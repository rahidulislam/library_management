from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import MemberApplication

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        token_data = super().validate(attrs)
        data = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.get_role_display(),
            'access': token_data['access'],
            'refresh': token_data['refresh']
        }

        
        return data

class MemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberApplication
        fields = ('id','first_name', 'last_name', 'email', 'phone', 'address',
                  'city', 'nid', 'birth_registration', 'image' )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = instance.get_image_url()
        data['status'] = instance.get_status_display()
        return data