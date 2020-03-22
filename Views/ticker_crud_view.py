from django.http import HttpResponseRedirect
from django.http.response import Http404, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import ProcessFormView
from django.views.generic.detail import DetailView
from Base.models import TicketBD
from Forms.form_ticket import get_form_ticket_bd ,TicketBDFormCreate
from django.contrib.auth.mixins import LoginRequiredMixin
from .view import MiximV
from django.urls import reverse
from django.shortcuts import redirect


class TicketUpdateView(MiximV, UpdateView):
    model = TicketBD
    template_name = "label/htmlForm/FormTicket.html"
    # fields = ['title', 'content', 'priority', 'groups', ]
    title = "Изменения заявки"

    def get_form_class(self):
        role = self.model.objects.get_role(self.request.user,self.get_object().pk)
        form = get_form_ticket_bd(role)
        return form

    def form_valid(self, form):
        employee = form.save()  # save form
        return redirect('ticket_detail', pk=self.get_object().pk)

class TicketCreateView(MiximV, CreateView):
    model = TicketBD
    # fields = ('title', 'content','groups', 'File')
    template_name = "label/htmlForm/FormTicket.html"
    success_url = '/'
    form_class = TicketBDFormCreate
    title = "Создания заявки"
    

    def form_valid(self, form):
        """Valid form """
        if form.is_valid():
            title = form.cleaned_data.get("title", None)
            content = form.cleaned_data.get("content", None)
            groups = form.cleaned_data.get("groups", None)
            # file = form.cleaned_data.get("File", None)
            autors = self.request.user

            self.model(title=title, content=content, 
                        groups=groups, autors=autors).save()
            return HttpResponseRedirect(self.success_url)


class TicketDeleteView(MiximV, DeleteView):
    model = TicketBD
    success_url = '/'
    template_name = "label/htmlForm/FormTicket.html"
    title = "Удаления заявки"
