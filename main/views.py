from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView

from blog.models import Blog
from emailapp import settings
from main.forms import MessageForm, ClientForm, MailingsForm
from main.models import Client, Logs, Message, Mailings
from main.services import get_client_cache
# from main.task import EmailTask


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_mailings'] = Mailings.objects.count()
        context['active_mailings'] = Mailings.objects.filter(status='started')
        context['count_clients'] = Client.objects.count()
        context['latest_posts'] = (Blog.objects.order_by('-date_published')[:3])
        context['most_viewed_posts'] = Blog.objects.order_by('-views_count')[:3]
        return context


# def index(request):
#     return render(request, 'main/index.html')


class ClientListView(PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'main/clients_list.html'
    context_object_name = 'clients_list'
    permission_required = 'main.view_client'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            context['client_list'] = get_client_cache(user=self.request.user)
        else:
            context['client_list'] = Client.objects.filter(owner=self.request.user)
        context['title'] = 'Клиенты'

        return context


class ClientsDetailView(PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'main.view_client'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Client
    template_name = 'main/clients_form.html'
    form_class = ClientForm
    permission_required = 'main.add_client'

    def get_success_url(self):
        return reverse_lazy('main:clients_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)


class ClientsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    template_name = 'main/clients_form.html'
    fields = ('__all__')
    permission_required = 'mail_sender.change_client'

    def get_object(self, *args, **kwargs):
        client = super().get_object(*args, **kwargs)
        if client.owners == self.request.user:
            return client
        return reverse_lazy('main:clients_list')

    def form_valid(self, form):
        if self.object.owner == self.request.user:
            self.object.owner = self.request.user
            self.object.save()
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:clients_list')


class ClientsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'main/clients_confirm_delete.html'
    permission_required = 'main.delete_client'

    def get_success_url(self):
        return reverse_lazy('main:clients_list')


class LogsListView(ListView):
    model = Logs
    template_name = 'main/logs_list.html'
    context_object_name = 'logs_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Логи'
        return context


# class LogsCreateView(CreateView):
#     model = Logs
#     template_name = 'main/logs_form.html'
#     form_class = LogsForm
#     success_url = reverse_lazy('main:logs_list')
#
#
# class LogsDetailView(DetailView):
#     model = Logs
#     template_name = 'main/logs_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
#
# class LogsUpdateView(UpdateView):
#     model = Logs
#     template_name = 'main/logs_form.html'
#     fields = ('__all__')
#
#     def get_success_url(self):
#         return reverse_lazy('main:logs_list')
#
#
# class LogsDeleteView(DeleteView):
#     model = Logs
#     template_name = 'main/logs_confirm_delete.html'
#
#     def get_success_url(self):
#         return reverse_lazy('main:logs_list')


class MessageListView(PermissionRequiredMixin, ListView):
    model = Message
    template_name = 'main/message_list.html'
    context_object_name = 'message_list'
    permission_required = 'main.view_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        return context


class MessageCreateView(PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    permission_required = 'main.add_message'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()
            return super().form_valid(form)


class MessageDetailView(PermissionRequiredMixin, DetailView):
    model = Message
    template_name = 'main/message_detail.html'
    permission_required = 'main.view_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MessageUpdateView(PermissionRequiredMixin, UpdateView):
    model = Message
    template_name = 'main/message_form.html'
    fields = ('__all__')
    permission_required = 'main.change_message'

    def form_valid(self, form):
        if self.object.owner == self.request.user:
            self.object.owner = self.request.user
            self.object.save()
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')


class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Message
    template_name = 'main/message_confirm_delete.html'
    permission_required = 'main.delete_message'

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')


class MailingsListView(PermissionRequiredMixin, ListView):
    model = Mailings
    template_name = 'main/mailings_list.html'
    context_object_name = 'mailings_list'
    permission_required = 'main.view_mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рассылки'
        return context


class MailingsCreateView(PermissionRequiredMixin, CreateView):
    model = Mailings
    template_name = 'main/mailings_form.html'
    form_class = MailingsForm
    success_url = reverse_lazy('main:mailings_list')
    permission_required = 'main.add_mailings'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)


class MailingsDetailView(DetailView):
    model = Mailings
    template_name = 'main/mailings_detail.html'
    permission_required = 'main.view_mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Mailings.objects.get(id=self.kwargs.get('pk')).clients.all()
        context['clients'] = clients
        return context


class MailingsUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailings
    form_class = MailingsForm
    template_name = 'main/mailings_form.html'
    permission_required = 'main.change_mailing'

    def form_valid(self, form):
        if self.object.owner == self.request.user:
            self.object.owner = self.request.user
            self.object.save()
            if form.is_valid():
                self.object = form.save()
                self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')


class MailingsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mailings
    template_name = 'main/mailings_confirm_delete.html'
    permission_required = 'main.delete_mailing'

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')
