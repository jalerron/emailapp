from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserResetPasswordForm(PasswordResetForm):

    class Meta:
        model = User
        fields = ('email',)