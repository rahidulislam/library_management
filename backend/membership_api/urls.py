from django.urls import path
from membership_api.views import (
    MemberApplicationListCreateView,
    AcceptMemberApplicationView,
    MemberDetailsView,
)

app_name = "membership_api"

urlpatterns = [
    path("details/", MemberDetailsView.as_view(), name="member_details"),
    path("application/", MemberApplicationListCreateView.as_view(), name="member_application_list_create"),
    path("application/accept/<int:pk>/", AcceptMemberApplicationView.as_view(), name="member_application_accept"),

]
