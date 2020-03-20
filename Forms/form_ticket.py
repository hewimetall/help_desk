from django import forms
from Base.models import TicketBD
from Base.models import CustomGroup
from .forms import CrispyModelFormMixim
from crispy_forms.layout import  Submit

class TicketBDFormCreate(CrispyModelFormMixim, forms.ModelForm):
    "('title', 'content','groups', 'File','priority')"
    groups = forms.ModelChoiceField(queryset=CustomGroup.objects.get_visible(),
                                    label="Департаменты")

class UserTicketBDFormUpdate(CrispyModelFormMixim, forms.ModelForm):
    class Meta:
        model = TicketBD
        fields = ['title', 'content',  'groups', ]

class ManegerTicketBDFormUpdate(CrispyModelFormMixim, forms.ModelForm):
    class Meta:
        model = TicketBD
        fields = [ 'groups', 'maneger','status']

class AnonTicketBDFormUpdate(CrispyModelFormMixim, forms.ModelForm):
    def setting(self):
        self.helper.add_input(Submit('принять', 'Принять заявку'))
    
    class Meta:
        model = TicketBD
        fields = []

class FormTicketBD(object):
    def __init__(self,role):
        self.role=role
        self.form=self.get_form(role)

    def get_form(self,role):
        

def get_form_ticket_bd(role):
    if role == "manager":
        return ManegerTicketBDFormUpdate
    if role == "autor":
        return UserTicketBDFormUpdate 
    if role == "anon":
        return AnonTicketBDFormUpdate