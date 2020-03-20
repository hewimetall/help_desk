from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import Http404, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import ProcessFormView
from django.views.generic.detail import DetailView
from Base.models import TicketBD ,TicketChat
from Forms.forms_chat import TicketChatForm


class TicketDetail(LoginRequiredMixin, DetailView,):
    template_name = "label/ticketDetail.html"
    model = TicketBD
    context_object_name = 'ticket'
    title = "Имформация о заявке"

    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['chat']     = self.get_chat_url()
        context['is_role']  = self.model.objects.get_role(self.request.user,self.get_object().pk)
        return context

    def get_chat_url(self):
        url = TicketChat.objects.filter(post=self.get_object().pk)
        return url


class TicketChatsView(LoginRequiredMixin, DetailView, ProcessFormView):
    """ Chat details for one ticket."""
    template_name = "label/chatDetail.html"
    model = TicketBD
    model2 = TicketChat
    chenge_form=TicketChatForm
    context_object_name = 'chat'
    title = "Чат заявки"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_forms(
            self.get_object().pk, self.request.user)
        return context

    def get_forms(self, pk, user):
        self.role = self.model.objects.get_role(user=user, pk=pk)
        form      = self.chenge_form.get_form(self.role)
        return form



# class ChatUserList(LoginRequiredMixin, ListAPIView):
#     serializer_class = ChatSerializer
#     queryset = ticketChat.objects.all()
#     template_name = "label/ticketDetail.html"

#     def get_queryset(self):
#         if 'pk' in self.kwargs:
#             pk = self.kwargs['pk']
#             try:
#                 tic = TicketBD.objects.vireficate_art(
#                     user=self.request.user, pk=pk)
#                 q = ticketChat.objects.filter(post=tic)
#                 return q
#             except TicketBD.DoesNotExist:
#                 return ticketChat.objects.none()
#             return ticketChat.objects.all()
