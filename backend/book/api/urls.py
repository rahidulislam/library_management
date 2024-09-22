from django.urls import path
from book.api.views import (
    AuthorListCreateAPIView,
    AuthorRetrieveUpdateDestroyAPIView,
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    BorrowingCreateAPIView,
    MemberBorrowingListAPIView,
    CheckBorrowingBookAPIView,
    ReturnBookAPIView,
)

app_name = "book_api"

urlpatterns = [
    path("authors/", AuthorListCreateAPIView.as_view(), name="author_list_create"),
    path(
        "authors/<int:pk>/",
        AuthorRetrieveUpdateDestroyAPIView.as_view(),
        name="author_retrieve_update_destroy",
    ),
    path("books/", BookListCreateAPIView.as_view(), name="book_list_create"),
    path(
        "books/<int:pk>/",
        BookRetrieveUpdateDestroyAPIView.as_view(),
        name="book_retrieve_update_destroy",
    ),
    path("borrowing/", BorrowingCreateAPIView.as_view(), name="borrowing_create"),
    path(
        "borrowing/member/",
        MemberBorrowingListAPIView.as_view(),
        name="member_borrowing_list",
    ),
    path(
        "borrowing/check/",
        CheckBorrowingBookAPIView.as_view(),
        name="check_borrowing_book",
    ),
    path("return/<str:borrow_id>/", ReturnBookAPIView.as_view(), name="return_book"),
]
