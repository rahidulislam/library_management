from rest_framework import serializers
from book.models import Author,Book

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