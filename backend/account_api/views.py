from django.shortcuts import render
from django.db.models import Q
from rest_framework import status,generics,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from account_api.serializers import MemberApplicationSerializer,MyTokenObtainPairSerializer
from account.models import MemberApplication
from backend.permissions import IsAdmin
# Create your views here.

class SignInView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
class MemberApplicationListCreateView(generics.ListCreateAPIView):
    queryset = MemberApplication.objects.all()
    serializer_class = MemberApplicationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdmin()]
        return [permissions.AllowAny()]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nid = serializer.validated_data.get('nid')
        birth_registration = serializer.validated_data.get('birth_registration')
        if MemberApplication.objects.filter(Q(nid=nid) | Q(birth_registration=birth_registration)).exists():
            return Response({'error': 'Member already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)