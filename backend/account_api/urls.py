from django.urls import path
from account_api.views import (
    AdminSignupView,
    MemberSignUpView,
    SignInView,
    # AcceptMemberApplicationView,
    # RejectMemberApplicationView,
    # ApplyMembershipView
)

app_name = "account_api"

urlpatterns = [
    path("member-signup/", MemberSignUpView.as_view(), name="user_signup"),
    path("admin-signup/", AdminSignupView.as_view(), name="admin_signup"),
    path("token/", SignInView.as_view(), name="token_obtain_pair"),
    # path(
    #     "membership/apply/",
    #     ApplyMembershipView.as_view(),
    #     name="apply_membership",
    # ),
    # path(
    #     "member/application/accept/<int:pk>/",
    #     AcceptMemberApplicationView.as_view(),
    #     name="member_application_accept",
    # ),
    # path(
    #     "member/application/reject/<int:pk>/",
    #     RejectMemberApplicationView.as_view(),
    #     name="member_application_reject",
    # ),
]
