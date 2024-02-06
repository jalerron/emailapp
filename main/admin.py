
from django.contrib import admin
from .models import Client, Logs, Mailings, Message

admin.site.register(Client),
admin.site.register(Logs),
admin.site.register(Mailings)
admin.site.register(Message)
