from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.permissions import IsAdmin,IsMember
from membership.models import Member
from book.models import Author,Book,Borrowing
from book.api.serializers import AuthorSerializer,BookSerializer,BorrowingSerializer,BorrowingListSerializer,CheckBorrowingSerializer
# Create your views here.
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'pk'
    http_method_names = ['get', 'patch', 'delete']
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    http_method_names = ['get', 'patch', 'delete']
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

class BorrowingCreateAPIView(generics.CreateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save()
        return Response({
            "message": "Borrow request created.",
            "borrow_id": borrowing.borrow_id  # Return borrow_id for the member
        }, status=status.HTTP_201_CREATED)
    
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
        return get_object_or_404(Borrowing,borrow_id=self.request.data.get('borrow_id'))

    
    