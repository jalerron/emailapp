from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView

from blog.models import Blog
from emailapp import settings
from main.forms import MessageForm, ClientForm, LogsForm, MailingsForm
from main.models import Client, Logs, Message, Mailings
from main.task import EmailTask


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


class ClientListView(ListView):
    model = Client
    template_name = 'main/clients_list.html'
    context_object_name = 'clients_list'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        return context


class ClientsDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ClientCreateView(CreateView):
    model = Client
    template_name = 'main/clients_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('main:clients_list')


class ClientsUpdateView(UpdateView):
    model = Client
    template_name = 'main/clients_form.html'
    fields = ('__all__')

    def form_valid(self, form):
        result = super().form_valid(form)
        try:
            EmailTask.send_emails()
        except Exception as e:
            messages.error(self.request, f'Ошибка при отправке рассылки: {e}')
        return result

    def get_success_url(self):
        return reverse_lazy('main:clients_list')


class ClientsDeleteView(DeleteView):
    model = Client
    template_name = 'main/clients_confirm_delete.html'

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


class LogsCreateView(CreateView):
    model = Logs
    template_name = 'main/logs_form.html'
    form_class = LogsForm
    success_url = reverse_lazy('main:logs_list')


class LogsDetailView(DetailView):
    model = Logs
    template_name = 'main/logs_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LogsUpdateView(UpdateView):
    model = Logs
    template_name = 'main/logs_form.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse_lazy('main:logs_list')


class LogsDeleteView(DeleteView):
    model = Logs
    template_name = 'main/logs_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('main:logs_list')


class MessageListView(ListView):
    model = Message
    template_name = 'main/message_list.html'
    context_object_name = 'message_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'main/message_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'main/message_form.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'main/message_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')


class MailingsListView(ListView):
    model = Mailings
    template_name = 'main/mailings_list.html'
    context_object_name = 'mailings_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рассылки'
        return context


class MailingsCreateView(CreateView):
    model = Mailings
    template_name = 'main/mailings_form.html'
    form_class = MailingsForm
    success_url = reverse_lazy('main:mailings_list')


class MailingsDetailView(DetailView):
    model = Mailings
    template_name = 'main/mailings_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MailingsUpdateView(UpdateView):
    model = Mailings
    template_name = 'main/mailings_form.html'
    fields = ('__all__')

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')


class MailingsDeleteView(DeleteView):
    model = Mailings
    template_name = 'main/mailings_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('main:mailings_list')
