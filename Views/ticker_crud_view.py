from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import Http404, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import ProcessFormView
from django.views.generic.detail import DetailView
from Base.models import TicketBD
from .forms import TicketBDFormUpdate, TicketBDFormCreate, GetTicketForm, TicketChatFormManeger, TicketChatFormAutors, TicketChat
from .models import ticketChat


class FormTicketUpdate(LoginRequiredMixin, UpdateView):
    model = TicketBD
    template_name = "label/htmlForm/FormTicket.html"
    form_class = TicketBDFormUpdate
    # fields = ['title', 'content', 'priority', 'groups', ]
    success_url = "/"

    def get_form_class(self):
        pass


class FormTicketCreate(LoginRequiredMixin, CreateView):
    model = TicketBD
    # fields = ('title', 'content','groups', 'File')
    template_name = "label/htmlForm/FormTicket.html"
    success_url = '/'
    form_class = TicketBDFormCreate

    def form_valid(self, form):
        """Valid form """
        if form.is_valid():
            title = form.cleaned_data.get("title", None)
            content = form.cleaned_data.get("content", None)
            groups = form.cleaned_data.get("groups", None)
            file = form.cleaned_data.get("File", None)
            priority = self.model.Priority[0][0]
            autors = self.request.user

            self.model(title=title, content=content, File=file,
                       priority=priority, groups=groups, autors=autors).save()
            return HttpResponseRedirect(self.success_url)


class FormTicketDelete(LoginRequiredMixin, DeleteView):
    model = TicketBD
    success_url = '/'
    template_name = "label/htmlForm/FormTicket.html"


class TicketDetail(LoginRequiredMixin, DetailView,):
    template_name = "label/ticketDetail.html"
    model = TicketBD
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat'] = self.get_chat_url()
        return context

    def get_chat_url(self,):
        url = ticketChat.objects.filter(post=self.get_object().pk)
        return url


class TicketChatsView(LoginRequiredMixin, DetailView, ProcessFormView):
    """docstring for TicketChatsView."""
    template_name = "label/chatDetail.html"
    model = TicketBD
    model2 = ticketChat
    context_object_name = 'chat'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_forms(
            self.get_object().pk, self.request.user)
        return context

    def get_forms(self, pk, user):
        self.role = self.model.objects.get_role(user=user, pk=pk)
        form = TicketChat().get_form(self.role)
        return form


class RestChatUpdate(View):
    http_method_names = ['get', 'post', ]
    model = TicketBD
    model2 = ticketChat
    form = TicketChat()

    def get():
        return Http404("error")

    def post(self, request, *args, **kwargs):
        # get form +
        # valid form +
        # save data +
        # return Okk +
        # print("test 0") +
        obj = self.get_object()
        # print("test 1") +
        form = self.get_form(pk=obj.pk, user=self.request.user)
        # print("test 2") +
        data = self.valid_form_try(form)
        if hasattr(data,"body"):
            self.push_a()
        # print("test 3") +
        self.save(data["status"], data["body"], data["name"], data["file"])
        # print("test 4") +
        return HttpResponse("ok")

    def get_form(self, pk, user):
        role = self.model.objects.get_role(user=user, pk=pk)
        form = self.form.get_form(name=role)
        return form

    def get_object(self):
        objects = self.model.objects.get(pk=self.kwargs['pk'])
        return objects

    def valid_form_try(self, form):
        forms = form(self.request.POST or None)
        if not forms.is_valid():
            raise ValueError("form is not  valid")
        if not hasattr(forms,'getSTATUS'):
            return forms.cleaned_data
        data=forms.cleaned_data
        data['name']=self.request.user
        data['status']=forms.getSTATUS(data)
        if not 'file' in data:
            data['file']=None
        return data


    def push_a(self):
            q = self.get_object()
            q.maneger = self.request.user
            q.save()


    def save(self, status, body, name, file):
        if status != None:
            q = self.get_object()
            q.status = status
            q.save()

            q2 = self.model2(post=self.get_object(),
                             name=name, body=body, file=file)
            q2.save()

class ChatUserList(LoginRequiredMixin, ListAPIView):
    serializer_class = ChatSerializer
    queryset = ticketChat.objects.all()
    template_name = "label/ticketDetail.html"

    def get_queryset(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            try:
                tic = TicketBD.objects.vireficate_art(
                    user=self.request.user, pk=pk)
                q = ticketChat.objects.filter(post=tic)
                return q
            except TicketBD.DoesNotExist:
                return ticketChat.objects.none()
            return ticketChat.objects.all()
