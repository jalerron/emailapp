from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import Group, Permission

from emailapp import settings
from users.forms import UserRegisterForm, UserResetPasswordForm, ManagerForm, ProfileAdminForm, UserUpdateForm, \
    ProfileUpdateForm
from users.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from users.services import register_confirm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form, *args, **kwargs):
        new_user = form.save()
        new_user.user_token = token_generator.make_token(new_user)
        form.save()
        register_confirm_ = register_confirm(self.request, user=new_user)
        if not new_user.is_active:
            send_mail(
                subject="Подтверждение почты",
                message=register_confirm_['message'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:verify_email')


class EmailVerifyView(View):
    success_url = 'users/verified_email.html'

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user

    def get(self, request, uidb64, user_token):

        user = self.get_user(uidb64)

        if user is not None and user.user_token == user_token:
            user.is_active = True
            user.is_staff = True
            user.save()

        try:
            users_group, created = Group.objects.get_or_create(name='Users')
            if created:
                permissions = Permission.objects.filter(
                    codename__in=['add_client', 'change_client', 'view_client', 'delete_client',
                                  'view_mailings', 'add_mailings', 'change_mailings',
                                  'delete_mailings',
                                  'add_message', 'change_message', 'view_message',
                                  'delete_message',
                                  'view_log', 'change_user', 'delete_user']
                )
                users_group.permissions.set(permissions)
            user.groups.add(users_group)
            user.save()

            return render(request, 'users/verified_email.html')
        except User.DoesNotExist:
            return render(request, 'users/incorrect_verify.html')


def verify_view(request):
    return render(request, 'users/verify_email.html')


class UserPasswordResetView(CreateView):
    model = User
    form_class = UserResetPasswordForm
    template_name = 'users/password_reset.html'
    success_url = 'users/password_reset_complete.html'

    def form_valid(self, form, *args, **kwargs):
        email_user = form['email']['value']
        pass_ = 'ASDqwe123'
        print(email_user)
        try:
            user = User.objects.get(email=email_user)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        if user is not None:
            send_mail(
                subject="Сброс пароля",
                message=f'Новый пароль: {pass_}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            user.password = pass_
            user.save()
            render(self.request, 'users/password_reset_complete.html')

        return super().form_valid(form)


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users_list'
    permission_required = 'users.view_user'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Manager').exists():
            queryset = queryset.filter(groups__name='Users')
            return queryset
        elif self.request.user.is_superuser:
            return queryset.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'users/users_detail.html'
    permission_required = 'users.view_user'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/users_form.html'
    permission_required = 'users.set_active'

    def get_form_class(self):
        if self.request.user.groups.filter(name='Manager').exists() and self.object.email == self.request.user.email:
            form_class = ProfileUpdateForm
        elif self.request.user.groups.filter(name='Manager').exists():
            form_class = ManagerForm
        elif self.request.user.is_superuser:
            form_class = ProfileAdminForm
        else:
            form_class = UserUpdateForm

        return form_class

    def form_valid(self, form):
        if form.has_changed():
            user = self.get_object()
            if user.is_active:
                user.is_active = False
            user.is_active = True
            user.save()
            form.save()
        return super().form_valid(form)

    def get_object(self, *args, **kwargs):
        user = super().get_object(*args, **kwargs)
        if (self.request.user.has_perm(self.permission_required) and self.request.user.is_staff) \
                or self.request.user.is_superuser:
            return user
        raise PermissionError


    def get_success_url(self):
        return reverse_lazy('users:users_list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/users_confirm_delete.html'
    success_url = reverse_lazy('users:users_list')
