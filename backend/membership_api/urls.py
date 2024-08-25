from django.urls import path
from membership_api.views import (
    MemberApplicationListCreateView,
)

app_name = "membership_api"

urlpatterns = [
    path("application/", MemberApplicationListCreateView.as_view(), name="member_application_list_create"),
]
