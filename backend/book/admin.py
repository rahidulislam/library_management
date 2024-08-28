from django.contrib import admin
from .models import Book, Borrowing
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','total_copies',)

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('id','member','book','borrowed_date','due_date',)
