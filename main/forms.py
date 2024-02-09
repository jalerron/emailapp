from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from main.models import Message, Client, Mailings
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class CrispyFormMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('owner',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


# class LogsForm(forms.ModelForm):
#     class Meta:
#         model = Logs
#         exclude = ('owner',)


class MailingsForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = Mailings
        exclude = ('owner', 'is_active')
        widgets = {
            'start_time': DateTimePickerInput(),
            'end_time': DateTimePickerInput()
        }

