from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms

from main.forms import CrispyFormMixin
from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserResetPasswordForm(PasswordResetForm):

    class Meta:
        model = User
        fields = ('email',)


class ManagerForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']


class ProfileAdminForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = User
        exclude = ['user_token', 'date_joined', 'first_name', 'last_name', 'password', 'last_login']


class UserUpdateForm(CrispyFormMixin, forms.ModelForm):
    model = User
    fields = ['username', 'phone', 'country', 'avatar',]


class ProfileUpdateForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone', 'country', 'avatar', 'is_active']