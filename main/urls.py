from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page


from main.apps import MainConfig
from main.views import ClientListView, LogsListView, MessageListView, MailingsListView, ClientsDetailView, \
    ClientsUpdateView, ClientsDeleteView, MailingsDetailView, \
    MailingsUpdateView, MailingsDeleteView, MessageDetailView, MessageDeleteView, MessageUpdateView, MessageCreateView, \
    ClientCreateView, MailingsCreateView, HomeView

app_name = MainConfig.name
urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('create_clients/', ClientCreateView.as_view(), name='clients_create'),
    path('client/<int:pk>/', ClientsDetailView.as_view(), name='clients_detail'),
    path('update_client/<int:pk>/', ClientsUpdateView.as_view(), name='clients_update'),
    path('client/<int:pk>/delete/', ClientsDeleteView.as_view(), name='clients_delete'),

    path('logs/', LogsListView.as_view(), name='logs_list'),
    # path('create_logs/', LogsCreateView.as_view(), name='logs_create'),
    # path('logs/<int:pk>/', LogsDetailView.as_view(), name='logs_detail'),
    # path('update_logs/<int:pk>/', LogsUpdateView.as_view(), name='logs_update'),
    # path('logs/<int:pk>/delete/', LogsDeleteView.as_view(), name='logs_delete'),

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('create_message/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),

    path('mailings/', MailingsListView.as_view(), name='mailings_list'),
    path('create_mailing/', MailingsCreateView.as_view(), name='mailings_create'),
    path('mailing/<int:pk>/', MailingsDetailView.as_view(), name='mailings_detail'),
    path('update_mailing/<int:pk>/', MailingsUpdateView.as_view(), name='mailings_update'),
    path('mailing/<int:pk>/delete/', MailingsDeleteView.as_view(), name='mailings_delete'),

]


for urlpattern in urlpatterns:
    if urlpattern.name not in ['home', 'blog']:
        urlpattern.callback = login_required(urlpattern.callback)