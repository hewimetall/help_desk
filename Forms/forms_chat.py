from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms
from Base.models import TicketBD
from .forms import CrispyModelFormMixim


# Form 
#    TicketChatForm
#           Template:
#               body ->  Сообщения
#    ManegerTicketChatForm
#               two bool fields
#    AutorsTicketChatForm
#               two bool fields
#    GetTicketForm
#               form for change manager
#    TicketChat 
#               Control class  

class TicketChatForm(CrispyModelFormMixim, forms.Form):
    # Template Chat Form
     
    body = forms.CharField(label='Сообщения')
    # file = forms.FileField(label='Файл', max_length=100, required=False)

    def setting(self):
        self.helper.add_input(Submit('отправить', 'Отправить',))


class ManegerTicketChatForm(TicketChatForm):
    is_move_ticket_back = forms.BooleanField(
        label="Отправить на доработку", required=False)
    is_move_ticket_end = forms.BooleanField(
        label="Выполнено тикет", required=False)

    def getSTATUS(self, form_clear_data):
        if form_clear_data['is_move_ticket_end'] and form_clear_data['is_move_ticket_back']:
            return None
        if form_clear_data['is_move_ticket_back']:
            return TicketBD.STATUS[1][0]
        if form_clear_data['is_move_ticket_end']:
            return TicketBD.STATUS[3][0]
        if "body" in form_clear_data:
            return TicketBD.STATUS[2][0]
        return None


class AutorsTicketChatForm(TicketChatForm):
    is_move_ticket_end = forms.BooleanField(
        label="Закрыть тикет", required=False)
    is_move_ticket_back = forms.BooleanField(
        label="Отправить на обработку", required=False)

    def getSTATUS(self, form_clear_data):
        if form_clear_data['is_move_ticket_end'] and form_clear_data['is_move_ticket_back']:
            return None
        if form_clear_data['is_move_ticket_back']:
            return TicketBD.STATUS[1][0]
        if form_clear_data['is_move_ticket_end']:
            return TicketBD.STATUS[4][0]
        if "body" in form_clear_data:
            return TicketBD.STATUS[2][0]
        raise ValueError

class GetTicketForm(CrispyModelFormMixim, forms.Form):

    def __init__(self, *args, **kwargs):
        super(GetTicketForm, self).__init__(*args, **kwargs)
        self.helper= FormHelper()
        self.helper.form_method= 'post'
        self.helper.form_action= ''
        self.helper.add_input(Submit('принять заявку', 'Принять заявку'))

    def getSTATUS(self, form_clear_data):
        raise ValueError



class TicketChatForm(object):

    def __init__(self):
        self.form_autor= AutorsTicketChatForm
        self.form_maneger= ManegerTicketChatForm
        self.form_new_form= GetTicketForm

    def get_form(self, role: str) -> TicketChatForm:
        if role == "maneger":
            return self.form_maneger
        if role == "autor":
            return self.form_autor
        if role == "anon":
            return self.form_new_form
        
