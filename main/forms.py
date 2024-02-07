from django import forms

from main.models import Message, Client, Logs, Mailings


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('__all__')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('__all__')


class LogsForm(forms.ModelForm):
    class Meta:
        model = Logs
        fields = ('__all__')


class MailingsForm(forms.ModelForm):
    class Meta:
        model = Mailings
        fields = ('__all__')

