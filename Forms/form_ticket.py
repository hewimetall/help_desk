from django import forms
from Base.models import TicketBD
from Base.models import CustomGroup
from .forms import CrispyModelFormMixim
from crispy_forms.layout import  Submit

class TicketBDFormCreate(CrispyModelFormMixim, forms.ModelForm):
    "('title', 'content','groups', 'File','priority')"

    class Meta:
        model = TicketBD
        fields = ['title', 'content',  'groups', ]
    
class UserTicketBDFormUpdate(CrispyModelFormMixim, forms.ModelForm):

    def save(self, commit=True):
        m = super(UserTicketBDFormUpdate, self).save(commit=False)
        if commit:
            m.status = 0
            m.save()
        return m
        
    class Meta:
        model = TicketBD
        fields = ['title', 'content',  'groups', ]

class ManegerTicketBDFormUpdate(CrispyModelFormMixim, forms.ModelForm):
    class Meta:
        model = TicketBD
        fields = [ 'groups', ]


    def save(self, commit=True):
        m = super(ManegerTicketBDFormUpdate, self).save(commit=False)
        if commit:
            m.status = 0
            m.menager = None
            m.save()
        return m

class AnonTicketBDFormUpdate(CrispyModelFormMixim, forms.ModelForm):
    def setting(self):
        self.helper.add_input(Submit('принять', 'Принять заявку'))
    
    class Meta:
        model = TicketBD
        fields = []


def get_form_ticket_bd(role):
    if role == "maneger":
        return ManegerTicketBDFormUpdate
    if role == "autor":
        return UserTicketBDFormUpdate 
    if role == "anon":
        return AnonTicketBDFormUpdate