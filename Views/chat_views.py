from django.http import HttpResponseRedirect
from django.http.response import Http404, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import ProcessFormView
from django.views.generic.detail import DetailView
from Base.models import TicketBD ,TicketChat
from Forms.forms_chat import TicketChatForm, GetTicketForm
from .view import MiximV

class TicketDetail(MiximV, DetailView,):
    template_name = "label/ticketDetail.html"
    model = TicketBD
    context_object_name = 'ticket'
    title = "Имформация о заявке"

    def get_object(self, queryset=None):
        obj = super(DetailView,self).get_object()
        if self.model.objects.vireficate_art(self.request.user,obj.pk) == None:
            raise Http404('Вы не принадлижите этой группе;)')
        return obj

    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['is_role']  = self.model.objects.get_role(self.request.user,self.get_object().pk)
        context['form_anon']=GetTicketForm
        return context

    def get_chat_url(self):
        url = TicketChat.objects.filter(post=self.get_object().pk)
        return url


class TicketChatView(MiximV, DetailView, ProcessFormView):
    """ Chat details for one ticket."""
    template_name = "label/chatDetail.html"
    model = TicketBD
    model2 = TicketChat
    chenge_form=TicketChatForm()
    context_object_name = 'chat'
    title = "Чат заявки"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_forms(
            self.get_object().pk, self.request.user)
        context['state'] = self.get_object().getStatus()
        context['role']  = self.role
        return context

    def get_forms(self, pk, user):
        self.role = self.model.objects.get_role(user=user, pk=pk)
        form      = self.chenge_form.get_form(self.role)
        return form

