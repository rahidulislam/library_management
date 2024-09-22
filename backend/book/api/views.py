from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.permissions import IsAdmin, IsMember
from membership.models import Member
from book.models import Author, Book, Borrowing
from book.api.serializers import (
    AuthorSerializer,
    BookSerializer,
    BorrowingSerializer,
    BorrowingListSerializer,
    CheckBorrowingSerializer,
)
from book.utils import generate_qr_code


# Create your views here.
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = "pk"
    http_method_names = ["get", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    http_method_names = ["get", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class BorrowingCreateAPIView(generics.CreateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsMember]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data.get("book", None)
        due_date = serializer.validated_data.get("due_date", None)
        member = get_object_or_404(Member, user=request.user)
        if Borrowing.objects.filter(
            member=member, book=book, is_returned=False
        ).exists():
            return Response(
                {"details": "This member has already borrowed this book."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Borrowing.objects.filter(book=book,returned_date__isnull=True,is_returned=False).count() >= book.total_copies:
            return Response(
                {"details": "No available copies of this book."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if due_date <= datetime.now().date():
            return Response(
                {
                    "details": "Due date cannot be in the past or today. Please select a future date."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing = serializer.save(member=member)
        qr_code_path = generate_qr_code(str(borrowing.borrow_id))
        borrowing.qr_code = qr_code_path
        borrowing.save()
        return Response(
            {
                "message": "Borrow request created.",
                "borrow_id": borrowing.borrow_id,
                "qr_code": borrowing.get_qr_code_url(),  # Return borrow_id for the member
            },
            status=status.HTTP_201_CREATED,
        )


class MemberBorrowingListAPIView(generics.ListAPIView):
    serializer_class = BorrowingListSerializer
    permission_classes = [IsMember]

    def get_queryset(self):
        member = get_object_or_404(Member, user=self.request.user)
        return Borrowing.objects.filter(member=member)


class CheckBorrowingBookAPIView(generics.RetrieveAPIView):
    serializer_class = CheckBorrowingSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        return get_object_or_404(
            Borrowing, borrow_id=self.request.data.get("borrow_id")
        )
