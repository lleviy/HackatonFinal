from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from django.urls import path, include

from .views import SignUpView, UsersView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('users/', UsersView.as_view(), name='users'),
]