from django.http.response import Http404, HttpResponse
from django.views.generic import View
from Base.models import TicketBD ,TicketChat 
from Forms.forms_chat import TicketChatForm

# Create your views here.
class RestChatUpdate(View):
    http_method_names = ['get', 'post', ]
    model = TicketBD
    model2 = TicketChat
    form = TicketChatForm()

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
