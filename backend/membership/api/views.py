from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.permissions import IsAdmin,IsMember

from membership.models import MemberApplication, Member, MemberSubscription
from membership.api.serializers import MemberApplicationSerializer,MemberApplicationListSerializer,MemberSerializer

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

class AcceptMemberApplicationView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        application = get_object_or_404(MemberApplication, pk=pk)
        if application.status != MemberApplication.Status.PENDING:
            return Response(
                {
                    "error": "Member application already approved or rejected"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        application.status = MemberApplication.Status.APPROVED
        application.save()
        member, created = Member.objects.get_or_create(user=application.user)
        MemberSubscription.objects.get_or_create(member=member, subscription_plan=application.subscription_plan)
        return Response({"details": "Member application accepted successfully"}, status=status.HTTP_200_OK)
    
class MemberDetailsView(generics.RetrieveAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsMember]

    
    def get_object(self):
        return get_object_or_404(Member.objects.prefetch_related('subscription', 'subscription__subscription_plan','subscription__subscription_plan__library_branch', 'subscription__subscription_plan__library_branch__library'), user=self.request.user)