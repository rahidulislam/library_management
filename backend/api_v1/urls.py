# myapi/urls.py
from django.urls import path, include
app_name = 'api_v1'
urlpatterns = [
    path('account/', include('account_api.urls', namespace='account_api')),
    path('member/', include('membership.api.urls', namespace='membership_api')),
    path('book/', include('book.api.urls', namespace='book_api'))  # Routes for app1's APIs
    # Include more apps as needed
]
