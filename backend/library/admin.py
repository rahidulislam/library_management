from django.contrib import admin
from .models import Library, LibraryBranch
# Register your models here.
admin.site.register(Library)
@admin.register(LibraryBranch)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'address', 'contact_number','library',)