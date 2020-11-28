from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic

from .models import User


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


class UsersView(ListView, PermissionRequiredMixin):
    template_name = 'users.html'
    model = User
    permission_required = 'accounts.view_user'