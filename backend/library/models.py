from django.db import models
from backend.base import TimeStamp


# Create your models here.
class Library(TimeStamp):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class LibraryBranch(TimeStamp):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="branches"
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.library.name} - {self.name}"
