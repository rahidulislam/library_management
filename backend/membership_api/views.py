from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from backend.permissions import IsAdmin,IsMember
from account.models import User
from membership.models import MemberApplication, SubscriptionPlan
from membership_api.serializers import MemberApplicationSerializer,MemberApplicationListSerializer

# Create your views here.
class MemberApplicationListCreateView(generics.ListCreateAPIView):
    queryset = MemberApplication.objects.all()
    serializer_class = MemberApplicationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdmin()]
        return [IsMember()]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if MemberApplication.objects.filter(user=request.user).exists():
            return Response(
                {
                    "error": "Member application already exists"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(user=request.user)
        return Response({"details": "Member application submited successfully"}, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return MemberApplicationSerializer
        return MemberApplicationListSerializer