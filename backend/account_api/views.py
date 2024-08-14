from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from account_api.serializers import (
    MemberApplicationSerializer,
    MyTokenObtainPairSerializer,
    RejectMemberApplicationSerializer,
)
from account.models import MemberApplication, User
from account_api.serializers import UserSerializer
from backend.permissions import IsAdmin
# Create your views here.


class MemberSignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.role = User.UserRoleType.MEMBER
        user.save()
        return user


class AdminSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_superuser = True
        user.is_staff = True
        user.role = User.UserRoleType.ADMIN
        user.save()
        return user


class SignInView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MemberApplicationListCreateView(generics.ListCreateAPIView):
    queryset = MemberApplication.objects.all()
    serializer_class = MemberApplicationSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdmin()]
        return [permissions.AllowAny()]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nid = serializer.validated_data.get("nid")
        birth_registration = serializer.validated_data.get("birth_registration")
        email = serializer.validated_data.get("email")
        if MemberApplication.objects.filter(
            Q(nid=nid) | Q(birth_registration=birth_registration)
        ).exists():
            return Response(
                {
                    "error": "Member application with this NID or Birth Registration already exists"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptMemberApplicationView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self):
        return get_object_or_404(MemberApplication, pk=self.kwargs.get("pk"))

    def post(self, request, *args, **kwargs):
        member_application = self.get_object()
        if member_application.status == MemberApplication.Status.PENDING:
            if User.objects.filter(email=member_application.email).exists():
                return Response(
                    {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create(
                first_name=member_application.first_name,
                last_name=member_application.last_name,
                email=member_application.email,
                role=User.MEMBER,
            )
            user.set_password(member_application.nid)
            user.save()
            member_application.user = user
            member_application.status = MemberApplication.Status.APPROVED
            member_application.save()
            return Response(
                {"message": "Member application approved successfully"},
                status=status.HTTP_200_OK,
            )
        elif member_application.status == MemberApplication.Status.APPROVED:
            return Response(
                {"error": "Member application already approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif member_application.status == MemberApplication.Status.REJECTED:
            return Response(
                {"error": "Member application is rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"error": "Invalid member application status"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RejectMemberApplicationView(generics.UpdateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = RejectMemberApplicationSerializer

    def get_object(self):
        return get_object_or_404(MemberApplication, pk=self.kwargs.get("pk"))

    def put(self, request, *args, **kwargs):
        member_application = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if member_application.status == MemberApplication.Status.PENDING:
            member_application.reject_feedback = serializer.validated_data.get(
                "reject_feedback"
            )
            member_application.status = MemberApplication.Status.REJECTED
            member_application.save()
            return Response(
                {"message": "Member application rejected successfully"},
                status=status.HTTP_200_OK,
            )
        elif member_application.status == MemberApplication.Status.APPROVED:
            return Response(
                {"error": "Member application already approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif member_application.status == MemberApplication.Status.REJECTED:
            return Response(
                {"error": "Member application already rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"error": "Invalid member application status"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MemberApplicationDetail(generics.RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = MemberApplicationSerializer

    def get_object(self):
        return get_object_or_404(MemberApplication, pk=self.kwargs.get("pk"))
