from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.response import Response
from account.serializers import MemberApplicationSerializer
from account.models import MemberApplication
# Create your views here.


class MemberApplicationListCreateView(generics.ListCreateAPIView):
    queryset = MemberApplication.objects.all()
    serializer_class = MemberApplicationSerializer