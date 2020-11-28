from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput

from .models import User
from django import forms

class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ("email",)