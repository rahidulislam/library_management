from django.urls import path
from book.api.views import AuthorListCreateAPIView,AuthorRetrieveUpdateDestroyAPIView,BookListCreateAPIView,BookRetrieveUpdateDestroyAPIView

app_name = "book_api"

urlpatterns = [
    path("authors/", AuthorListCreateAPIView.as_view(), name="author_list_create"),
    path("authors/<int:pk>/", AuthorRetrieveUpdateDestroyAPIView.as_view(), name="author_retrieve_update_destroy"),
    path("books/", BookListCreateAPIView.as_view(), name="book_list_create"),
    path("books/<int:pk>/", BookRetrieveUpdateDestroyAPIView.as_view(), name="book_retrieve_update_destroy"),
]