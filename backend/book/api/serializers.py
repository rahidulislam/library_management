from rest_framework import serializers
from book.models import Author,Book,Borrowing
from datetime import datetime

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','title', 'authors', 'isbn', 'publication_date', 'genre', 'total_copies')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['available_copies'] = instance.available_copies
        return data

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ('id','member', 'book', 'due_date', )

    def validate(self, attrs):
        book = attrs.get('book')
        due_date = attrs.get('due_date')
        member = attrs.get('member')
        if book.borrowings.filter(member=member, is_returned=False).exists():
            raise serializers.ValidationError({"details":"This member has already borrowed this book."})
        if book.borrowings.filter(is_returned=False).count() >= book.total_copies:
            raise serializers.ValidationError({"details":"No available copies of this book."})
        if due_date <= datetime.now().date():
            raise serializers.ValidationError({"details":"Due date cannot be in the past or today. Please select a future date."})
        return attrs

class BorrowingListSerializer(BorrowingSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update({
            "book": instance.book.title,
            "member": instance.member.user.email,
            "borrowed_date": instance.borrowed_date.strftime("%Y-%m-%d"),
            "borrow_id": instance.borrow_id,
            "is_returned": instance.is_returned
        })
        return data
class CheckBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ('borrow_id', )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update({
            "id": instance.id,
            "book": instance.book.title,
            "member": instance.member.user.email,
            "borrowed_date": instance.borrowed_date.strftime("%Y-%m-%d"),
            "due_date": instance.due_date.strftime("%Y-%m-%d"),
            "is_returned": instance.is_returned,
            "returned_date": instance.returned_date
        })
        return data