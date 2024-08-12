from django.urls import path
from account_api.views import MemberApplicationListCreateView,SignInView
app_name = 'account_api'

urlpatterns = [
    path('token/', SignInView.as_view(), name='token_obtain_pair'),
    path('member/application/', MemberApplicationListCreateView.as_view(), name='member_application'),

]