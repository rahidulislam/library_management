# myapi/urls.py
from django.urls import path, include
app_name = 'api_v1'
urlpatterns = [
    path('account/', include('account_api.urls', namespace='account_api')),
    path('member/', include('membership_api.urls', namespace='membership_api')),  # Routes for app1's APIs
    # Include more apps as needed
]
