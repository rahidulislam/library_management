from django.db import models
from backend.base import TimeStamp
from library.models import LibraryBranch
from membership.models import Member


# Create your models here.
class Author(TimeStamp):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name"]


class Book(TimeStamp):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    genre = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class BranchBook(TimeStamp):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="branch_books"
    )
    library_branch = models.ForeignKey(
        LibraryBranch, on_delete=models.CASCADE, related_name="branch_books"
    )
    available_copies = models.PositiveIntegerField(default=1)
    total_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} at {self.library_branch.name}"


class Borrowing(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="borrowings"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(blank=True, null=True)
    library_branch = models.ForeignKey(
        LibraryBranch, on_delete=models.CASCADE, related_name="borrowings"
    )

    # def is_overdue(self):
    #     return self.returned_date is None and self.due_date < date.today()

    def __str__(self):
        return f"{self.member.user.username} - {self.book.title}"


class Return(models.Model):
    borrowing = models.OneToOneField(
        Borrowing, on_delete=models.CASCADE, related_name="return_books"
    )
    returned_date = models.DateField()

    def __str__(self):
        return f"{self.borrowing.member.user.username} - {self.borrowing.book.title} returned"
