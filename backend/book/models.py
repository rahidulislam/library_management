from django.db import models
import uuid
from backend.base import TimeStamp
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
    total_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    @property
    def available_copies(self):
        return (
            self.total_copies
            - Borrowing.objects.filter(
                book=self, returned_date__isnull=True, is_returned=False
            ).count()
        )


class Borrowing(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="borrowings"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    borrow_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    # def is_overdue(self):
    #     return self.returned_date is None and self.due_date < date.today()

    def __str__(self):
        return f"{self.member.user.username} - {self.book.title}"

    def get_qr_code_url(self):
        return self.qr_code.url if self.qr_code else None
