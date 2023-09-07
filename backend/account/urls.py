from django.urls import path
from account.views import MemberApplicationListCreateView
app_name = 'account'

urlpatterns = [
    path('member/application/', MemberApplicationListCreateView.as_view(), name='member_application'),
]
